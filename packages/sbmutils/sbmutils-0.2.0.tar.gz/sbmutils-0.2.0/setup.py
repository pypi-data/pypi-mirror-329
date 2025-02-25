from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sbmutils",
    version="0.2.0",
    author="dalee",
    description="A collection of utility functions for data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dalee/sbmutils",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "scipy",
    ],
) 