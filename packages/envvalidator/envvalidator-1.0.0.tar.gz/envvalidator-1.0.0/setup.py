# SPDX-License-Identifier: Apache-2.0
# Author: Qiyaya

from setuptools import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

module = Extension(
    "envvalidator",
    sources=["main.cpp"],
)

setup(
    name="envvalidator",
    version="1.0.0",
    description="envvalidator description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Qiyaya",
    author_email="v2020.bohus.peter@gmail.com",
    url = 'https://github.com/Sekiraw/Envvalidator',
    keywords=["env", "validator", "validate", "environment"],
    license="Apache-2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    ext_modules=[module],
)
