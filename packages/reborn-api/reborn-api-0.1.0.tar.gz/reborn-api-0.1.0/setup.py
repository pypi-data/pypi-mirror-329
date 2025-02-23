from setuptools import setup, find_packages
import os
setup(
    name="reborn-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "telethon>=1.24.0"
    ],
    python_requires=">=3.8",
    author="HEHABICb",
    author_email="loliconschick@gmail.com",
    description="Api For Reborn Tool",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)