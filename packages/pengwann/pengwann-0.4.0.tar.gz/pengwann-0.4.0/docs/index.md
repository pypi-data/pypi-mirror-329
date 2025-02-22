# pengWann - Descriptors of chemical bonding from Wannier functions

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Docs](https://readthedocs.org/projects/pengwann/badge/?version=latest)](https://pengwann.readthedocs.io/en/latest/)
[![Test coverage](https://api.codeclimate.com/v1/badges/10626c706c7877d2af47/test_coverage)](https://codeclimate.com/github/PatrickJTaylor/pengWann/test_coverage)
[![Requires Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)](https://python.org/downloads)
[![PyPI version](https://badge.fury.io/py/pengwann.svg)](https://badge.fury.io/py/pengwann)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

`pengwann` is a lightweight Python package for calculating descriptors of chemical bonding and local electronic structure from Wannier functions (as obtained from [Wannier90](https://wannier.org/)).

More specifically, `pengwann` can be used to calculate the WOHP (Wannier Orbital Hamilton Population) and/or the WOBI (Wannier Orbital Bond index) between a pair (or larger cluster) of atoms. These quantities are analogous to the pCOHP (projected Crystal Orbital Hamilton Population) and pCOBI (projected Crystal Orbital Bond Index) implemented in the [LOBSTER](http://www.cohp.de/) code, except that the local basis we choose to represent the Hamiltonian and the density matrix is comprised of Wannier functions rather than pre-defined atomic or pseudo-atomic orbitals. This choice of a Wannier basis has the advantage that (for energetically isolated bands) **the spilling factor is strictly 0**. For further details as to the advantages and disadvantages of using a Wannier basis, as well as the mathematical formalism behind `pengwann` in general, please see the [Methodology](./methodology) page.

Besides the [API reference](./api), a detailed use case of how `pengwann` can be used to derive WOHPs, WOBIs and the pDOS can be found on the [Examples](./examples) page.

```{figure} _static/example_outputs_light.svg
:align: center
:class: only-light
:scale: 140%
```

```{figure} _static/example_outputs_dark.svg
:align: center
:class: only-dark
:scale: 140%
```

<center>
<small>
A handful of example outputs from <code>pengwann</code> as applied to rutile. The colour-coded numbers next to the crystal structure are Löwdin-style charges computed for Ti (blue) and O (red).
</small>
</center>

```{toctree}
---
hidden: True
---

installation
methodology
examples
api
CONTRIBUTING
```
