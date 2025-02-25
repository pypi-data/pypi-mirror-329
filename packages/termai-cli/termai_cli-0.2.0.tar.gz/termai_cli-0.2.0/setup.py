# setup.py
from setuptools import setup, find_packages

setup(
    name="termai-cli",  # Changed from termai to avoid conflicts
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "rich",
        "pydantic",
        "google-generativeai",
        "python-dotenv",
        "langchain-google-genai"
    ],
    entry_points={
        "console_scripts": [
            "termai=src.cli:app",
        ],
    },
    author="Ayush Gupta",
    author_email="ayush4002gupta@gmail.com",
    description="AI-powered CLI for generating and executing shell commands",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ayushgupta4002/termai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
)

