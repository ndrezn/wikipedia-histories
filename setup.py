# -*- coding: utf-8 -*-
import setuptools
from setuptools import find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="wikipedia_histories",
    version="1.1.0",
    author="Nathan Drezner",
    author_email="nathan@drezner.xyz",
    description="A Python tool to pull the complete edit history of a Wikipedia page",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ndrezn/wikipedia-histories",
    install_requires=[
        "aiohttp>=3.8.0",
        "lxml==4.9.1",
        "mwclient==0.10.1",
        "mwparserfromhell==0.6",
        "pandas>=1.2.3",
        "wikipedia-api==0.5.4",
    ],
    package_dir={"": "src"},
    packages=find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={"networks": ["networkx>=2.6", "python-igraph==0.9.1"]},
    python_requires=">=3.6",
)
