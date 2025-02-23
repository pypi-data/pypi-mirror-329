from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="genaitopic",
    version="0.1.3",
    description="A package for auto topic generation and prediction using RAG & LLMs.",
    author="Vishal Jadhav",
    author_email="vishalsjadhav53@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "pandas",
        "scikit-learn",
        "langchain","datetime"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
