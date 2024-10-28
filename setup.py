from setuptools import setup, find_packages
import os

setup(
    name='project1',
    version='1.0',
    author='Tanmay Saxena',
    author_email='tanmaysaxena@ufl.edu',
    packages=find_packages(exclude=('tests', 'docs')),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
        "spacy",
        "torch",
        "transformers",
        "pytest",
        "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.5.0/en_core_web_sm-3.5.0.tar.gz"
    ]
)

# Download model within setup if needed
try:
    import spacy
    spacy.cli.download("en_core_web_sm")
except ImportError:
    pass
