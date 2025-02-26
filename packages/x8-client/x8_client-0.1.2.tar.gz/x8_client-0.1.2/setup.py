"""Setup script for x8-client."""

from setuptools import setup, find_packages
import os
import re

# Get version without importing the package
def get_version():
    with open(os.path.join("x8", "__init__.py"), "r") as f:
        content = f.read()
    version_match = re.search(r'^__version__ = ["\']([^"\']*)["\']', content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="x8-client",
    version=get_version(),
    author="vubakninh",
    author_email="vubakninh@gmail.com",
    description="Client library for the x8 video processing API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/duvu/x8-client",
    project_urls={
        "Bug Tracker": "https://github.com/duvu/x8-client/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests",
        "python-dotenv",
    ],
    extras_require={
        "dev": [
            "pytest",
            "requests-mock",
            "pytest-mock",
            "pytest-cov",
            "twine",
            "build",
        ],
    },
)
