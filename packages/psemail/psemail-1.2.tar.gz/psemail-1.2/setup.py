#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="psemail",
    version="1.2",
    packages=find_packages(include=['psemail', 'psemail.*']),
    install_requires=[
        "python-dotenv"
    ],
    url="https://github.com/LaythOud/psemail",
    python_requires='>=3.6',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
)
