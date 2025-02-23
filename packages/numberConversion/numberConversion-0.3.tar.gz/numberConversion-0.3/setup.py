from setuptools import setup, find_packages
VERSION = '0.0.3'
DESCRIPTION = 'A simple package to convert binary to decimal and decimal to binary'
LONG_DESCRIPTION = 'A simple package to convert binary to decimal and decimal to binary'

setup(
    name="numberConversion",
    version="0.3",
    packages=find_packages(),
    install_requires=[],
    author="Prayush Shrestha",
    author_email="prayushshrestha89@gmail.com",
    description="A simple package to convert decimal to binary and binary to decimal",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shresthaprayush2/numberconversion.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
