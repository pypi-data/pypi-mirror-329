from setuptools import setup, find_packages

setup(
    name = "yet_another_hello_pypi",
    version = "0.0.2",
    author = "pygumby",
    description = "An example Python package deployed to PyPI",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/pygumby/yet_another_hello_pypi",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.6",
)
