[![License](https://img.shields.io/pypi/l/NuPaAc?color=blue)](https://codeberg.org/Cs137/NuPaAc/src/branch/main/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/NuPaAc.svg)](https://pypi.org/project/NuPaAc/)
[![PyPI Downloads](https://static.pepy.tech/badge/nupaac)](https://pepy.tech/projects/nupaac)


# NuPaAc - Nuclide Pandas Accessor

This python package provides the `NuclideSeriesAccessor` class, which acts as kind
of wrapper to interact with
[radioactivedecay `Nuclide`](https://radioactivedecay.github.io/nuclide.html?highlight=nuclide#id1)
objects from nuclide strings containing pandas `Series`. For detailed information
about the radioactivedecay package, see its [documentation](https://radioactivedecay.github.io/).

The series accessor allows to retrive several data series obtained from the dataset
in use by `radioactivedecay`. Where appropriate, data are returned as
[pint series](https://codeberg.org/Cs137/NuPaAc/src/branch/main/tutorial.md#pint-series),
allowing to preserve the unit and perform unit-aware operations.
The functionality is implemented via the [`pint-pandas` package](https://github.com/hgrecco/pint-pandas).

__Consult the [`tutorial.md` file](https://codeberg.org/Cs137/NuPaAc/src/branch/main/tutorial.md)
to learn about the functionality provided by this package.__


```{warning}
The project is currently under development and changes in its behaviour might be introduced.
```


## Installation

Install the latest release of NuPaAc from [PyPI](https://pypi.org/project/nupaac/)
via `pip`:

```sh
$ pip install nupaac
```

The development version can be installed from
[the Git repository](https://codeberg.org/Cs137/NuPaAc) using `pip`:

```sh
# Via https
pip install git+https://codeberg.org/Cs137/NuPaAc.git

# Via ssh
pip install git+ssh://git@codeberg.org:Cs137/NuPaAc.git
```


## Usage

The pandas `Series` accessor is available via the `nucs` attribute of Series
instances. In order to make use of the accessor, import the module `nucs` from
this package.

__Examples demonstrating several use cases can be found in the
[`tutorial.md` file](https://codeberg.org/Cs137/NuPaAc/src/branch/main/tutorial.md).__


## Changes

All notable changes to this project are documented in the
[`CHANGELOG.md` file](https://codeberg.org/Cs137/NuPaAc/src/branch/main/CHANGELOG.md).


## Contributing

Contributions to the `NuPaAc` package are very welcomed. Feel free to submit a
pull request, if you would like to contribute to the project. In case you are
unfamiliar with the process, consult the
[forgejo documentation](https://forgejo.org/docs/latest/user/pull-requests-and-git-flow/)
and follow the steps using this repository instead of the `example` repository.

Create your [pull request (PR)](https://codeberg.org/Cs137/NuPaAc/pulls) to
inform that you start working on a contribution. Provide a clear description
of your envisaged changes and the motivation behind them, prefix the PR's title
with ``WIP: `` until your changes are finalised.

All kind of contributions are appreciated, whether they are
bug fixes, new features, or improvements to the documentation.


## Development

### Installing for development

To install the package in development mode, clone the Git repository and install
the package using Poetry, as shown in the code block underneath. To install Poetry,
which is required for virtual environment and dependency management, follow the
instructions on the [Poetry website](https://python-poetry.org/docs/#installation).

```bash
git clone https://codeberg.org/Cs137/NuPaAc.git
cd nupaac
poetry install
```

This will create a virtual environment and install the package dependencies and
the package itself in editable mode, allowing you to make changes to the code and
see the effects immediately in the corresponding virtual environment. Alternatively,
you can install it via `pip install -e` in an existing virtual environment.


## License

NuPaAc is open source software released under the MIT License.
See [LICENSE](https://codeberg.org/Cs137/NuPaAc/src/branch/main/LICENSE) file for details.

---

This package was created and is maintained by Christian Schreinemachers, (C) 2025.
