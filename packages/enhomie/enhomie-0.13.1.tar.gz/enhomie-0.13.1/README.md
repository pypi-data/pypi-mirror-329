# Enasis Network Homie Automate

> :warning: This project has not released its first major version.

Define desired scenes for groups using flexible conditional plugins.

<a href="https://pypi.org/project/enhomie"><img src="https://enasisnetwork.github.io/enhomie/badges/pypi.png"></a><br>
<a href="https://enasisnetwork.github.io/enhomie/validate/flake8.txt"><img src="https://enasisnetwork.github.io/enhomie/badges/flake8.png"></a><br>
<a href="https://enasisnetwork.github.io/enhomie/validate/pylint.txt"><img src="https://enasisnetwork.github.io/enhomie/badges/pylint.png"></a><br>
<a href="https://enasisnetwork.github.io/enhomie/validate/ruff.txt"><img src="https://enasisnetwork.github.io/enhomie/badges/ruff.png"></a><br>
<a href="https://enasisnetwork.github.io/enhomie/validate/mypy.txt"><img src="https://enasisnetwork.github.io/enhomie/badges/mypy.png"></a><br>
<a href="https://enasisnetwork.github.io/enhomie/validate/yamllint.txt"><img src="https://enasisnetwork.github.io/enhomie/badges/yamllint.png"></a><br>
<a href="https://enasisnetwork.github.io/enhomie/validate/pytest.txt"><img src="https://enasisnetwork.github.io/enhomie/badges/pytest.png"></a><br>
<a href="https://enasisnetwork.github.io/enhomie/validate/coverage.txt"><img src="https://enasisnetwork.github.io/enhomie/badges/coverage.png"></a><br>
<a href="https://enasisnetwork.github.io/enhomie/validate/sphinx.txt"><img src="https://enasisnetwork.github.io/enhomie/badges/sphinx.png"></a><br>

## Documentation
Read [project documentation](https://enasisnetwork.github.io/enhomie/sphinx)
built using the [Sphinx](https://www.sphinx-doc.org/) project.
Should you venture into the sections below you will be able to use the
`sphinx` recipe to build documention in the `sphinx/html` directory.

## Useful and related links
- [Philips Hue API](https://developers.meethue.com/develop/hue-api-v2/api-reference)
- [Ubiquiti API](https://ubntwiki.com/products/software/unifi-controller/api)

## Installing the package
Installing stable from the PyPi repository
```
pip install enhomie
```
Installing latest from GitHub repository
```
pip install git+https://github.com/enasisnetwork/enhomie
```

## Quick start for local development
Start by cloning the repository to your local machine.
```
git clone https://github.com/enasisnetwork/enhomie.git
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

## Running the service
There are several command line arguments, see them all here.
```
python -m enhomie.execution.service --help
```
Here is an example of running the service from inside the project folder
within the [Workspace](https://github.com/enasisnetwork/workspace) project.
```
python -m enhomie.execution.service \
  --config ../../Persistent/enhomie-prod.yml \
  --console \
  --debug \
  --respite_update 120 \
  --respite_desire 15 \
  --timeout_stream 120 \
  --idempotent \
  --print_desire \
  --print_aspire
```
Replace `../../Persistent/enhomie-prod.yml` with your configuration file.

## Deploying the service
It is possible to deploy the project with the Ansible roles located within
the [Orchestro](https://github.com/enasisnetwork/orchestro) project! Below
is an example of what you might run from that project to deploy this one.
However there is a bit to consider here as this requires some configuration.
```
make -s \
  limit=all \
  orche_files=../../Persistent/orchestro-prod.yml \
  ansible_args=" --diff" \
  enhomie-install
```

## Version management
> :warning: Ensure that no changes are pending.

1. Rebuild the environment.
   ```
   make -s check-revenv
   ```

1. Update the [version.txt](enhomie/version.txt) file.

1. Push to the `main` branch.

1. Create [repository](https://github.com/enasisnetwork/enhomie) release.

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
