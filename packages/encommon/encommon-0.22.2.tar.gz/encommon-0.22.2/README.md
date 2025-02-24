# Enasis Network Common Library

> :warning: This project has not released its first major version.

Common classes and functions used in various public and private projects.

<a href="https://pypi.org/project/encommon"><img src="https://enasisnetwork.github.io/encommon/badges/pypi.png"></a><br>
<a href="https://enasisnetwork.github.io/encommon/validate/flake8.txt"><img src="https://enasisnetwork.github.io/encommon/badges/flake8.png"></a><br>
<a href="https://enasisnetwork.github.io/encommon/validate/pylint.txt"><img src="https://enasisnetwork.github.io/encommon/badges/pylint.png"></a><br>
<a href="https://enasisnetwork.github.io/encommon/validate/ruff.txt"><img src="https://enasisnetwork.github.io/encommon/badges/ruff.png"></a><br>
<a href="https://enasisnetwork.github.io/encommon/validate/mypy.txt"><img src="https://enasisnetwork.github.io/encommon/badges/mypy.png"></a><br>
<a href="https://enasisnetwork.github.io/encommon/validate/yamllint.txt"><img src="https://enasisnetwork.github.io/encommon/badges/yamllint.png"></a><br>
<a href="https://enasisnetwork.github.io/encommon/validate/pytest.txt"><img src="https://enasisnetwork.github.io/encommon/badges/pytest.png"></a><br>
<a href="https://enasisnetwork.github.io/encommon/validate/coverage.txt"><img src="https://enasisnetwork.github.io/encommon/badges/coverage.png"></a><br>
<a href="https://enasisnetwork.github.io/encommon/validate/sphinx.txt"><img src="https://enasisnetwork.github.io/encommon/badges/sphinx.png"></a><br>

## Documentation
Read [project documentation](https://enasisnetwork.github.io/encommon/sphinx)
built using the [Sphinx](https://www.sphinx-doc.org/) project.
Should you venture into the sections below you will be able to use the
`sphinx` recipe to build documention in the `sphinx/html` directory.

## Projects using library
- [Enasis Network Remote Connect](https://github.com/enasisnetwork/enconnect)
- [Enasis Network Homie Automate](https://github.com/enasisnetwork/enhomie)
- [Enasis Network Chatting Robie](https://github.com/enasisnetwork/enrobie)
- [Enasis Network Orchestrations](https://github.com/enasisnetwork/orchestro)

## Installing the package
Installing stable from the PyPi repository
```
pip install encommon
```
Installing latest from GitHub repository
```
pip install git+https://github.com/enasisnetwork/encommon
```

## Quick start for local development
Start by cloning the repository to your local machine.
```
git clone https://github.com/enasisnetwork/encommon.git
```
Set up the Python virtual environments expected by the Makefile.
```
make -s venv-create
```

### Execute the linters and tests
The comprehensive approach is to use the `check` recipe. This will stop on
any failure that is encountered.
```
make -s check
```
However you can run the linters in a non-blocking mode.
```
make -s linters-pass
```
And finally run the various tests to validate the code and produce coverage
information found in the `htmlcov` folder in the root of the project.
```
make -s pytest
```

## Version management
> :warning: Ensure that no changes are pending.

1. Rebuild the environment.
   ```
   make -s check-revenv
   ```

1. Update the [version.txt](encommon/version.txt) file.

1. Push to the `main` branch.

1. Create [repository](https://github.com/enasisnetwork/encommon) release.

1. Build the Python package.<br>Be sure no uncommited files in tree.
   ```
   make -s pypackage
   ```

1. Upload Python package to PyPi test.
   ```
   make -s pypi-upload-test
   ```

1. Upload Python package to PyPi prod.
   ```
   make -s pypi-upload-prod
   ```
