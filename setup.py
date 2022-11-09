import setuptools
from setuptools import find_packages

with open("requirements.txt", mode="r") as file:
    requirements = file.read().split("\n")


setuptools.setup(
    name="CNN_Spotify_Music",
    version="0.0.1",
    description="Apache Beam pipeline that uses Convolutional Neural Networks to predict music genre from audio files",
    classifiers=[
        "Intended Audience :: W207 - Fall 2022 - Section 04",
        "Programming Language :: Python :: 3.8",
        "Topic :: Experience :: Final Project"
    ],
    packages=find_packages() + ['.'],
    install_requires = requirements,
    python_requires = '>=3.8'
)