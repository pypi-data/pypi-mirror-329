from setuptools import setup, find_packages

setup(
    name='shc_utilities',                 # Package name (the one you will install via pip)
    #version=setuptools_scm.get_version(),  # Automatically get the version from Git tags
    version="0.1.1",
    packages=find_packages(where='.'),       # Find all sub-packages recursively
    install_requires=[                   # Add any external dependencies you need here
        # 'some_dependency>=1.0.0',
    ],
    include_package_data=True,           # Include non-Python files like README.md if needed
    description='Utilities for working config and logger',  # Optional
)