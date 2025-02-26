import os

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="identt",
    version=os.getenv("PACKAGE_VERSION", "0.1.0"),
    packages=find_packages(where="."),
    package_dir={"": "."},
    install_requires=["requests"],
    author="brdge.ai",
    description="Python SDK for Iden API interactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
