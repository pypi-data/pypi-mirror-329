# Remote script service tools package for python

## Usage

```python

```

## Development
[Python packaging docs](https://packaging.python.org/en/latest/tutorials/packaging-projects/#a-simple-project)

### Build

Windows
```bash
py -m pip install --upgrade build
py -m build
```
Linux
```bash
python3 -m pip install --upgrade build
python3 -m build
```

### Publish

Windows
```bash
py -m pip install --upgrade twine
py -m twine upload --repository testpypi dist/*
```
Linux
```bash
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```

