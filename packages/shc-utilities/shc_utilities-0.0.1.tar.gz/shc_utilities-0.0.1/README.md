# python-shc-lib
```
pip install git+https://gitlab.com/straw-hat-crew/python-shc-lib.git@0.1.0
```

```
pip install setuptools_scm
pip install --upgrade pip setuptools
pip install --upgrade wheel
pip cache purge
```

### for Linux
```
cd ~
touch .pypirc
```
### for Windows
```
cd %USERPROFILE%
type NUL > .pypirc
```
### Edit .pypirc file by copying and pasting the following configuration
```
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-
```
*** Replace with the actual API token you generated from PyPI. Do not forget to include the pypi- prefix. ***

### Ensure you have a setup.py file in your project’s root directory. Run the following command to create distribution files
```
pip install twine
python setup.py sdist bdist_wheel
twine upload dist/*
```