# setup.py
import os
from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="netdots",
    version="0.1.0",
    packages=find_packages(include=["netdots", "netdots.*"], exclude=["netdots.oros", "netdots.oros.*"]),
    install_requires=["requests"],  
    author="Netdots",
    author_email="support@netdots.com",
    description="Netdots Library - A Python SDK for interacting with the Netdots API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://netdots.com",  # ✅ Fixed GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
