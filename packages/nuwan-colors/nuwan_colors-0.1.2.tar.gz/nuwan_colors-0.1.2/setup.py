# setup.py
from setuptools import setup, find_packages

setup(
    name="nuwan_colors",
    version="0.1.2",
    packages=find_packages(),
    description="A lightweight package for adding customizable text coloring and styling to terminal output, making console applications more visually appealing and readable",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Shashika Nuwan (DevShashika)",
    author_email="shashika90nuwan@gmail.com",
    url="https://github.com/DevNuwancat/NuwanColors.git",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
        
)