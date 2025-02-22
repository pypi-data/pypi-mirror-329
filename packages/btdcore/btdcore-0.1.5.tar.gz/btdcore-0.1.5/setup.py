#!/usr/bin/env python

from setuptools import find_packages, setup



setup(
    name="btdcore",
    version="v0.1.5",
    description="Core Python library for BlackTuskData",
    author="Liam Tengelis",
    author_email="liam.tengelis@blacktuskdata.com",
    packages=find_packages(),
    package_data={
        "": ["*.yaml"],
        "btdcore": [
            "py.typed",
        ],
    },
    install_requires=[
        "pydantic",
        "requests",
    ],
)
