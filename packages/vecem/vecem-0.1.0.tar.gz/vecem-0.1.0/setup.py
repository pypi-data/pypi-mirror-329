
from setuptools import setup, find_packages

setup(
    name='vecem',
    version='0.1.0',
    author='vecem',
    author_email='vectorembeddings@gmail.com',
    description='A simple library to download datasets from vecem using Azure Blob Storage.',
    long_description='A library to easily download datasets from Azure Blob Storage.',
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'requests',
        'tqdm'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
