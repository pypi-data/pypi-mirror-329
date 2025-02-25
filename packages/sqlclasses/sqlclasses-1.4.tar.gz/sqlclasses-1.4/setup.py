#!/usr/bin/env python3
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlclasses",
    version="1.4",
    author="Diedrich Vorberg",
    author_email="diedrich@tux4web.de",
    description="Construct SQL commands and queries using Python classes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dvorberg/sqlclasses",

    packages=setuptools.find_packages(),
    include_package_data=False,

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
