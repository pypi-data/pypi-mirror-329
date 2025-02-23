# setup.py
from setuptools import setup
setup(
    name="barre",
    version="1.0.5",
    py_modules=["barre"],
    description="Minimal progress bar",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Fonk",
    author_email="feelthefonk@gmail.com",
    url="https://github.com/FeelTheFonk/barre",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)