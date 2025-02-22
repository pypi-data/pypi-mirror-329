from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="timetrix",
    version="0.0.7",
    entry_points={
        "console_scripts": [
            "timetrix=timetrix.cli:main",
        ],
    },
    author="Maglovski Nenad",
    author_email="maglovskin@gmail.com",
    description="Lightweight and intuitive Python library designed to help developers,track, measure, and visualize time with ease.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maglovskiNenad/timetrix",
    packages=find_packages(),
    install_requires=[
        "datetime",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)