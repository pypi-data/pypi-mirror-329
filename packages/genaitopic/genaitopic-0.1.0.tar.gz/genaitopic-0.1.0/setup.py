from setuptools import setup, find_packages

setup(
    name="genaitopic",
    version="0.1.0",
    description="A package for auto topic generation and prediction using LLMs.",
    author="Vishal Jadhav",
    author_email="vishalsjadhav53@gmail.com",
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
