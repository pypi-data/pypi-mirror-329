# flacfixer
A program to automatically manage the filenames of your music
directory.

[![builds.sr.ht status](https://builds.sr.ht/~rensoliemans/flacfixer.svg)](https://builds.sr.ht/~rensoliemans/flacfixer?)

## Install

    git clone https://git.sr.ht/~rensoliemans/flacfixer
    pip install .

Or, if you'd like to run linters,

    pip install .[dev]

Or, if you want an [editable
install](https://setuptools.pypa.io/en/latest/userguide/development_mode.html),

    pip install -e .

## Run

    $ flacfixer --help
    usage: flacfixer [-h] (-a | -f) [-n] [-r RECURSE_LEVELS] [-v]

    Fix filenames in my music dir

    options:
      -h, --help            show this help message and exit
      -a, --albums          Fixes album names (directories) in PWD
      -f, --filenames       Fixes filenames in PWD
      -n, --dry-run         Perform dry run and output what would be changed
      -r RECURSE_LEVELS, --recurse-levels RECURSE_LEVELS
                            Levels to recurse into. Defaults to 0, current level
      -v, --verbose         Be verbose. Pass multiple times to increase verbosity


This is specific to my music library and preferences:

### Filenames
`flacfixer -f` changes the filenames of music files. Only `flac` is
currently supported. The target is `{tracknumber} - {title}.flac`,
where `tracknumber` always has length `2`. `tracknumber` and `title`
are extracted from metadata.

Example: `01 - Rosalyn.flac`

### Albums
`flacfixer -a` changes the directory names into the following format:
`{album name} [{year}]`. Since a directory itself can't have any
metadata, it attempts to parse the title and year from the current
directory format. See
[test_album_fixer.py](https://git.sr.ht/~rensoliemans/flacfixer/tree/main/item/test/test_album_fixer.py).

Example: `Tripping with Nils Frahm [2020]`

## Contributions
### Code style
[![Code style:
black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This project uses [black](https://black.readthedocs.io/en/stable/),
[ruff](https://github.com/charliermarsh/ruff) and
[pre-commit](https://pre-commit.com/). They are all installed when you
do `pip install -e .[dev]`.

Install `pre-commit` hooks with

    pre-commit install

`make` commands:
- `make lint`: executes `black` and `ruff`. This is also more or less
what `pre-commit` does.

- `make analyse`: `make lint` and `mypy`

- `make test`: unittests

- `make check`: `make analyse` and `make test` (everything)

### Contributing
I'm new to mailing lists with git, but please send patches to
[~rensoliemans/flacfixer@lists.sr.ht](mailto:~rensoliemans/flacfixer@lists.sr.ht).
