# IForth

Forth kernel for Jupyter notebook / lab. This is a fork of [github.com/jdfreder/iforth](https://github.com/jdfreder/iforth).

[Open in Colab](https://colab.research.google.com/github/sohang3112/iforth/blob/master/forth_jupyter_tour.ipynb)

![Example Notebook Screenshot](notebook_screenshot.png)

**Note:** Check the [changelog](CHANGELOG.md) to see the latest changes in development as well as in releases.

## Installation

- Install pre-reequisites: `python3`, `gforth` (forth interpreter).
- Run `pip install forth_kernel`.
- Now register it with jupyter: `python -m forth_kernel.self_install --user`.

**Note:** On Windows, `gforth` doesn't work. Instead, [run using docker](#installing-with-docker).

### Development Installation

Git clone this repo, then do editable install using [uv](https://github.com/astral-sh/uv): `uv run python -m forth_kernel.self_install --user`.

## Usage

- Run `jupyter notebook` (or `jupyter lab`, whichever you prefer).
- In a new or existing notebook, use the kernel selector (located at the top right of the notebook) to select `IForth`.
