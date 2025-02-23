# plottica

[![PyPI - Version](https://img.shields.io/pypi/v/plottica.svg)](https://pypi.org/project/plottica)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/plottica.svg)](https://pypi.org/project/plottica)
[![PyPI - WIP](https://img.shields.io/badge/status-WIP-yellow.svg)](https://pypi.org/project/plottica)
[![pre-commit](https://github.com/LovelyBuggies/plottica/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/LovelyBuggies/plottica/actions)
[![tests](https://github.com/LovelyBuggies/plottica/actions/workflows/tests.yml/badge.svg)](https://github.com/LovelyBuggies/plottica/actions)
-----

`plottica` is a Python package that provides elegant shortcuts for academic plotting.

## Installation

We only support PyPI installation yet.

```bash
pip install plottica
```

## Usage

```python
WIP
```

## Contributing

You are welcome to add more functionalities or develop based on this package, feel free to [PR](https://github.com/LovelyBuggies/plottica/pulls).

Here is the workflow for your development:

1. Create a venv or conda env for development
2. Add optional-dependencies to `./pyproject.toml`
3. `pip install -e ".[dev]"`
4. Add a module to `./src/plottica`
5. Write a usage tutorial to `./tutorials` and build it with `jupyter-book build ./tutorials`
6. Add tests to `./tests`
7. if new hooks are added, `pre-commit clean && pre-commit install && pre-commit run --all-files`
9. Upload to your GitHub repo, PR, and wait for review

Then, I will upload to PyPI,
1. New version at `./src/plottica/__about__.py`
2. `python -m build` 
3. `twine upload dist/*`


## Acknowledgement

This package is heavily based on [Matplotlib](https://matplotlib.org/stable/) and [Seaborn](https://seaborn.pydata.org/). The documentation is built with [Jupyter Book](https://jupyterbook.org/intro.html). 