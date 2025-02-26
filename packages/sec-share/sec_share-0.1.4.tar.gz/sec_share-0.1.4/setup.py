from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sec-share",
    version="0.1.4",
    author="Ritisha Bhattacharjee",
    author_email="ritish200302@gmail.com",
    description="A CLI tool to securely share code snippets with automatic secret detection and redaction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ritishab0209/sec",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "sec-share=sec_share.cli:main",
        ],
    },
)