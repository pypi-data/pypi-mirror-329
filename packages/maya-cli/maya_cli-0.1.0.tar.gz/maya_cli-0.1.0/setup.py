# setup.py 

from setuptools import setup, find_packages

setup(
    name="maya-cli",
    version="0.1.0",
    author="King Anointing Joseph Mayami",
    author_email="anointingmayami@gmail.com",
    description="Maya CLI - AI Project Generator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/anointingmayami/Maya.ai",
    packages=find_packages(),
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "maya=maya.cli:maya",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
