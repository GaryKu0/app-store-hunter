from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="app-store-icon-hunter",
    version="2.0.0",
    author="Developer",
    author_email="developer@example.com",
    description="A powerful CLI tool and API for searching apps and downloading icons from App Store and Google Play",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/app-store-icon-hunter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "requests>=2.25.0",
        "Pillow>=8.0.0",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "aiohttp>=3.8.0",
        "aiofiles>=0.8.0",
        "python-multipart>=0.0.5",
        "pydantic>=1.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "icon-hunter=app_store_icon_hunter.cli.main:cli",
        ],
    },
)