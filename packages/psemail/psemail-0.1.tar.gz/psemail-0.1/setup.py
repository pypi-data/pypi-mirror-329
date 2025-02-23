from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="psemail",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "python-dotenv"
    ],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
