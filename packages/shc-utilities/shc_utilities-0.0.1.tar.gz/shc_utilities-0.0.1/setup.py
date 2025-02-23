from setuptools import setup, find_packages
import os

version = os.getenv('VERSION', '0.0.0')  # Default to '0.0.0' if the environment variable is not set

setup(
    name='shc_utilities',                 # Package name (the one you will install via pip)
    #version=setuptools_scm.get_version(),  # Automatically get the version from Git tags
    version=version, # Use the version retrieved from Git
    packages=find_packages(where='.'),       # Find all sub-packages recursively
    install_requires=[                   # Add any external dependencies you need here
        # 'some_dependency>=1.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    include_package_data=True,           # Include non-Python files like README.md if needed
    description='Utilities for working config and logger',  # Optional
    author='Onkar Antad',
    author_email='onkarantad@gmail.com',
    url='https://gitlab.com/straw-hat-crew/python-shc-lib',
)