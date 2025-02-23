from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="snelnotuleren-sdk",
    version="1.1.6",
    author="Snelnotuleren.nl",
    author_email="niels@snelnotuleren.nl",
    description="Python SDK voor de Snelnotuleren.nl API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/snelnotuleren/python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    keywords="notulen, transcriptie, api, webhook",
)