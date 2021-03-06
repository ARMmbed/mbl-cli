#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Setuptools entry point."""

from setuptools import setup, find_packages


def read(file_name):
    """Read a file, return the contents as a str."""
    with open(file_name, "r") as readme:
        return readme.read()


def readlines(file_name):
    """Read a file, return the contents as a list."""
    with open(file_name, "r") as txt_file:
        return txt_file.readlines()


setup(
    name="mbl-cli",
    version="2.0.1",
    description="Mbed Linux OS Command Line Tool",
    long_description=read("README.md"),
    author="Arm Ltd.",
    license="BSD-3-Clause",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=readlines("requirements.txt"),
    include_package_data=True,
    zip_safe=False,
    entry_points={"console_scripts": ["mbl-cli = mbl.cli.mbl_cli:_main"]},
)
