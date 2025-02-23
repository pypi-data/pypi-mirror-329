from setuptools import setup, find_packages
import os
with open("README.md", "r") as fh:
    long_description = fh.read()

version = "1.0.1"
setup(
    name="databloom",
    version=version,
    author="gada121982",
    author_email="gada121982@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'v1': ["v1/*"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pandas",
        "psycopg2-binary"
        "sqlalchemy"
        "requests"
    ]
)
