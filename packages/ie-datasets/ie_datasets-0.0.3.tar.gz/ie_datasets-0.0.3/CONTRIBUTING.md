# Contributing

## Getting Started

```sh
# set up whatever virtual environment
pip install -r requirements.txt
pip install -e .
pip install build
pip install twine
```

We recommend symlinking your cache directory (e.g. `~/.local/share/ie_datasets`) to `cache` in this directory.
`.gitignore` is set up to automatically ignore that path.

```sh
ln -s /home/${USER}/.local/share/ie_datasets cache
```

## Publishing

```sh
python3 -m build
python3 -m twine upload dist/*
```
