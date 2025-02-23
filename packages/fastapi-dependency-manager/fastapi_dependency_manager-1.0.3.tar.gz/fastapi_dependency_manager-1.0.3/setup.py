from setuptools import setup, find_packages

setup(
    name="fastapi_dependency_manager",
    version="1.0.3",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "azure-storage-blob",
        "python-dotenv",
        "retry",
        "aiofiles",
        "pydantic",
        "requests",
        "typer",
        "rich",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "fastapi-dependency-manager=fastapi_dependency_manager.main:main",
            "dep-manager-cli=fastapi_dependency_manager.cli:app",
        ],
    },
    description="API to manage and upload Python dependencies",
    author="Kanav Arora",
    author_email="kanavlt885@gmail.com",
    url="https://github.com/Kanav-1822/fastapi-dependency-manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)