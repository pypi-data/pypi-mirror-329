from setuptools import setup, find_packages

setup(
    name="timetrix",
    version="0.0.4",
    entry_points={
        "console_scripts": [
            "timetrix=timetrix.cli:main",
        ],
    },
    author="Maglovski Nenad",
    author_email="maglovskin@gmail.com",
    description="Lightweight and intuitive Python library designed to help developers,track, measure, and visualize time with ease.",
    long_description=open("DOCUMENTATION.md").read(),
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