# setup.py 
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="maya-cli",
    version="0.1.1",
    author="King Anointing Joseph Mayami",
    author_email="anointingmayami@gmail.com",
    description="Maya CLI - AI Project Generator",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/anointingmayami/Maya.ai",
    packages=find_packages(),
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "maya=maya_cli.cli:maya",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
