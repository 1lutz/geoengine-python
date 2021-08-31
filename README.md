# Geo Engine Python Package


[![CI](https://github.com/geo-engine/geoengine-python/actions/workflows/ci.yml/badge.svg)](https://github.com/geo-engine/geoengine-python/actions/workflows/ci.yml)

This package allows easy access to Geo Engine functionality from Python environments.

## Test

Create a virtual environment (e.g., `python3 -m venv env`).
Then, install the dependencies with:

```bash
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
```

Run tests with:

```bash
pytest
```

## Dependencies

Since we use `cartopy`, you need to have the following system dependencies installed.

- GEOS
- PROJ

For Ubuntu, you can use this command:

```bash
sudo apt-get install libgeos-dev libproj-dev
```

## Build

You can build the package with:

```bash
python3 -m pip install --upgrade build
python3 -m build
```

## Formatting

This packages is formatted according to `pycodestyle`.
You can check it by calling:

```bash
python3 -m pycodestyle
```

Our tip is to install `autopep8` and use it to format the code.

## Lints

Our CI automatically checks for lint errors.
We use `pylint` to check the code.
You can check it by calling:

```bash
python3 -m pylint geoengine
python3 -m pylint tests
```

Our tip is to activate linting with `pylint` in your IDE.

## Distribute to PyPI

### Test-PyPI

```
python3 -m build
python3 -m twine upload --repository testpypi dist/*
```

### PyPI

```
python3 -m build
python3 -m twine upload --repository pypi dist/*
```

## Try it out

Start a python terminal and try it out:

```python
import geoengine as ge
from datetime import datetime

ge.initialize("http://peter.geoengine.io:6060")

time = datetime.strptime('2014-04-01T12:00:00.000Z', "%Y-%m-%dT%H:%M:%S.%f%z")

workflow = ge.workflow_by_id('4cdf1ffe-cb67-5de2-a1f3-3357ae0112bd')

print(workflow.get_result_descriptor())

workflow.get_dataframe(ge.Bbox([-60.0, 5.0, 61.0, 6.0], [time, time]))
```
