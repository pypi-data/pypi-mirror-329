import os
import logging
import subprocess
import time
from functools import lru_cache
from typing import List, Dict
from fastapi import FastAPI, File, UploadFile, HTTPException, status
import aiofiles
from azure.storage.blob import BlobServiceClient
from pydantic import BaseModel
from dotenv import load_dotenv
from retry import retry

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FastAPI Dependency Manager",
    description="API to manage and upload Python dependencies",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}


AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME", "dependency-cache")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_files")

os.makedirs(UPLOAD_DIR, exist_ok=True)

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

if not container_client.exists():
    container_client.create_container()


class DependencyInstallResponse(BaseModel):
    message: str
    details: List[str]


@lru_cache(maxsize=50)
def is_dependency_installed(dep: str) -> bool:
    result = subprocess.run(["pip", "show", dep], capture_output=True, text=True)
    return result.returncode == 0


@retry(tries=3, delay=2, backoff=2, logger=logger)
def download_from_azure(blob_client, download_path: str) -> None:
    with open(download_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())


def check_disk_space() -> bool:
    stat = os.statvfs(UPLOAD_DIR)
    free_space = stat.f_bavail * stat.f_frsize
    return free_space > 1024 * 1024 * 100


def cleanup_old_packages(max_age_days: int = 30) -> None:
    current_time = time.time()
    for file in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, file)
        file_age = current_time - os.path.getmtime(file_path)
        if file_age > max_age_days * 86400:
            os.remove(file_path)
            logger.info(f"Deleted old file: {file}")


@app.post("/upload/", status_code=status.HTTP_201_CREATED)
async def upload_requirements(file: UploadFile = File(...)) -> Dict[str, str]:
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
        logger.info(f"File {file.filename} uploaded successfully")
        return {"message": "File uploaded successfully", "filename": file.filename}
    except Exception as e:
        logger.error(f"Error uploading file {file.filename}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="File upload failed",
        )


@app.get("/dependencies/", response_model=List[str])
def list_dependencies(filename: str) -> List[str]:
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    with open(file_path, "r") as f:
        dependencies = [dep.strip() for dep in f.readlines()]

    return dependencies


@app.post("/install/", response_model=DependencyInstallResponse)
def install_dependencies(filename: str) -> DependencyInstallResponse:
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    with open(file_path, "r") as f:
        dependencies = [dep.strip() for dep in f.readlines()]

    installed_dependencies = []
    for dep in dependencies:
        if is_dependency_installed(dep):
            installed_dependencies.append(f"{dep} is already installed, skipping.")
            continue

        blob_name = f"{dep}.whl"
        blob_client = container_client.get_blob_client(blob_name)

        if blob_client.exists():
            download_path = os.path.join(UPLOAD_DIR, blob_name)
            try:
                download_from_azure(blob_client, download_path)
                subprocess.run(["pip", "install", download_path], check=True)
                installed_dependencies.append(
                    f"Installed {dep} from Azure Blob Storage"
                )
            except Exception as e:
                installed_dependencies.append(
                    f"Failed to install {dep} from Azure Blob Storage: {e}"
                )
                logger.error(f"Error installing {dep} from Azure Blob Storage: {e}")
        else:
            try:
                subprocess.run(["pip", "install", dep], check=True)
                installed_dependencies.append(f"Installed {dep} from PyPI")

                subprocess.run(
                    ["pip", "wheel", "--wheel-dir", UPLOAD_DIR, dep], check=True
                )

                for wheel_file in os.listdir(UPLOAD_DIR):
                    if wheel_file.endswith(".whl"):
                        wheel_file_path = os.path.join(UPLOAD_DIR, wheel_file)
                        with open(wheel_file_path, "rb") as data:
                            blob_client = container_client.get_blob_client(wheel_file)
                            blob_client.upload_blob(data, overwrite=True)
                            logger.info(f"Uploaded {wheel_file} to Azure Blob Storage")
            except subprocess.CalledProcessError as e:
                installed_dependencies.append(f"Failed to install {dep}: {e}")
                logger.error(f"Error installing {dep}: {e}")

    return DependencyInstallResponse(
        message="Dependency installation completed", details=installed_dependencies
    )


@app.delete("/azure/delete/")
def delete_cached_package(blob_name: str) -> Dict[str, str]:
    blob_client = container_client.get_blob_client(blob_name)
    if blob_client.exists():
        blob_client.delete_blob()
        logger.info(f"Deleted cached package: {blob_name}")
        return {"message": f"Deleted cached package: {blob_name}"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Package not found"
        )


@app.get("/azure/list/", response_model=List[str])
def list_azure_dependencies() -> List[str]:
    blobs = [blob.name for blob in container_client.list_blobs()]
    return blobs


@app.post("/cleanup/", status_code=status.HTTP_200_OK)
def cleanup_local_files() -> Dict[str, str]:
    try:
        cleanup_old_packages()
        logger.info("Local storage cleaned up successfully")
        return {"message": "Local storage cleaned up successfully"}
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clean up local storage",
        )


@app.get("/health/", status_code=status.HTTP_200_OK)
def health_check() -> Dict[str, str]:
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
