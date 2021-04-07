# -*- coding: utf-8 -*-

# python3 setup.py sdist bdist_wheel
# twine upload --skip-existing dist/*

import codecs
import os
import setuptools


def local_file(file):
    return codecs.open(os.path.join(os.path.dirname(__file__), file), "r", "utf-8")


with open("README.md", "r") as fh:
    long_description = fh.read()

install_reqs = [
    line.strip()
    for line in local_file("requirements.txt").readlines()
    if line.strip() != ""
]

setuptools.setup(
    name="wikipedia_histories",
    version="1.0.0",
    author="Nathan Drezner",
    author_email="nathan@drezner.com",
    description="A simple package designed to collect the edit histories of Wikipedia pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ndrezn/wikipedia-histories",
    install_requires=install_reqs,
    packages=["wikipedia_histories"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
