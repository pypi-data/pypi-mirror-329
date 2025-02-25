---
jupytext:
  formats: md:myst,ipynb
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.6
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Welcome to echemdb-converters's documentation!

`echemdbconverters` provides a modular API for loading non-standardized DSV (data-separated value) or CVS (comma-separated value) files, commonly created from software used to operate laboratory equipment.
Key issues of these files are, for example, lengthy header lines containing various metadata relevant to the recording software,
the use of `,` as a decimal separator in some regions of this world,
or files containing multiple data tables, etc.

`echemdbconverters` provides a mean to load data directly as a `pandas` Data Frame and allows conversion of data via a CLI into frictionless Data Packages (or [unitpackages](https://github.com/echemdb/) supporting the use of units) for seamless integration in existing workflows.

Our approach aims at providing a single interface to load data into a certain format independent of the data source.
Filetypes supported and tested by `echemdbconverters` are:

| Manufacturer | Device type  | Software                    | Filesuffix | Loader      | device |
|--------------|--------------|-----------------------------|------------|-------------|--------|
| Biologic     | Potentiostat | EClab                       | mpt        | EClabLoader | eclab  |
| Gamry        | Potentiostat | Gamry Instruments Framework | DTA        | GamryLoader | gamry  |
|              |              |                             |            |             |        |

```{todo}
Improve table, such as including links.
```

## Examples

Consider the following DSV. It consists of three parts:

* the header usually contains metadata relevant to the software and user predefined settings.
* column header lines containing acronyms (dimensions) and often units for the data in one ore more rows
* the data block, where each column consists of identical data types

```{code-cell} ipython3
:tags: [hide-input]

from io import StringIO
file = StringIO('''# I am messy data
Random stuff
maybe metadata : 3
in different formats = abc123
hopefully, some information
on where the data block starts!
t\tE\tj
s\tV\tA/cm2
0\t0\t0
1\t1\t1
2\t2\t2
''')
from echemdbconverters.baseloader import BaseLoader
csv = BaseLoader(file, header_lines=6, column_header_lines=2)
file.seek(0)
print(csv.file.read())
```

A pandas Data Frame can be created with limited input data.
The delimiter of the data block is evaluated using the [`clevercsv`](https://clevercsv.readthedocs.io/en/latest/index.html) module (unless specified).
Multiple column headers will be flattened.

```{code-cell} ipython3
from echemdbconverters.baseloader import BaseLoader
csv = BaseLoader(file, header_lines=6,
                 column_header_lines=2,
                 delimiters=None,
                 decimal=None)
csv.df
```

All parts of the file are accessible from the API for further use. For example the extraction of metadata from the header.

```{code-cell} ipython3
print(csv.header.read())
```

```{code-cell} ipython3
print(csv.column_headers.read())
```

```{code-cell} ipython3
print(csv.data.read())
```

The data can also be converted into frictionless Data Packages using the CLI.

```{note}
The input and output files for and from the following commands can be found in the [test folder](https://github.com/echemdb/echemdb-converters/tree/master/test/) of the repository.

The CLI only works for standard CSV without header and a single column header line, and specific converters summarized above.
```

A "standard" CSV

```{code-cell} ipython3
!echemdbconverters csv ../test/data/default.csv --outdir ../test/generated
```

A specific file type, including additional YAML metadata.

```{code-cell} ipython3
:tags: [remove-output]
!echemdbconverters csv ../test/data/eclab_cv.mpt --device eclab --metadata ../test/data/eclab_cv.mpt.metadata --outdir ../test/generated
```

## Further usage

Use echemdbs' `unitpackage` to browse, modify and visualize the Data Packages.

```{code-cell} ipython3
from unitpackage.collection import Collection
db = Collection.from_local('../test/generated')
entry = db['eclab_cv']
entry
```

## Installation

This package is available on [PiPY](https://pypi.org/project/echemdbconverters/) and can be installed with pip:

```sh .noeval
pip install echemdbconverters
```

See the [installation instructions](installation.md) for further details.

<!--
You can cite this project as described [on our zenodo page](https://zenodo.org/badge/latestdoi/XXXXXX).
-->

## License

The contents of this repository are licensed under the [GNU General Public
License v3.0](https://www.gnu.org/licenses/gpl-3.0.html) or, at your option, any later version.

+++

```{toctree}
:maxdepth: 2
:caption: "Contents:"
:hidden:
installation.md
cliusage.md
api.md
```
