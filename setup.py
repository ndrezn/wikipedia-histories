# -*- coding: utf-8 -*-

# python3 setup.py sdist bdist_wheel
# twine upload --skip-existing dist/*

import codecs
import os
import setuptools
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

install_reqs = [
    "aiohttp==3.7.4.post0",
    "lxml==4.6.5",
    "mwclient==0.10.1",
    "mwparserfromhell==0.6",
    "networkx==2.5.1",
    "pandas==1.2.3",
    "python-igraph==0.9.1",
    "wikipedia-api==0.5.4",
]

setuptools.setup(
    name="wikipedia_histories",
    version="1.1.0",
    author="Nathan Drezner",
    author_email="nathan@drezner.xyz",
    description="A simple package designed to collect the edit histories of Wikipedia pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ndrezn/wikipedia-histories",
    install_requires=install_reqs,
    tests_require=["pytest"],
    package_dir={"": "src"},
    packages=find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
