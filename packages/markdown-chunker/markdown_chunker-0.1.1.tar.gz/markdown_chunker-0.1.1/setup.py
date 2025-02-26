#!/usr/bin/env python
"""
Setup script for markdown-chunker.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="markdown-chunker",
    version="0.1.1",
    author="Saeed Hajebi",
    author_email="hajebis@tcd.ie",
    description="A tool for chunking markdown documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hadjebi/markdown_chunker",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pyyaml>=5.1",
    ],
    entry_points={
        "console_scripts": [
            "markdown-chunker=markdown_chunker.cli:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
        ],
    },
)
