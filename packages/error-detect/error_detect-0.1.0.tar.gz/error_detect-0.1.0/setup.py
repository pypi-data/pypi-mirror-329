# setup.py
from setuptools import setup, find_packages

# Ensure README.md is read with UTF-8 encoding
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="error_detect",
    version="0.1.0",
    author="Rahul Gond",
    author_email="27rg2000@gmail.com",
    description="A package for detecting errors and generating solutions using an LLM API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rhul27/error_detect",  # Update with your repository URL
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
