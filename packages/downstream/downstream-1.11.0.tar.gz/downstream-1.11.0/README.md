# Downstream --- Python Implementation

![downstream wordmark](https://raw.githubusercontent.com/mmore500/downstream/master/docs/assets/downstream-wordmark.png)

[![CI](https://github.com/mmore500/downstream/actions/workflows/python-ci.yaml/badge.svg?branch=python)](https://github.com/mmore500/downstream/actions/workflows/python-ci.yaml?query=branch:python)
[![GitHub stars](https://img.shields.io/github/stars/mmore500/downstream.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/mmore500/downstream)
[
![PyPi](https://img.shields.io/pypi/v/downstream.svg)
](https://pypi.python.org/pypi/downstream)
[![DOI](https://zenodo.org/badge/776865597.svg)](https://zenodo.org/doi/10.5281/zenodo.10866541)

downstream provides efficient, constant-space implementations of stream curation algorithms.

-   Free software: MIT license

<!---
-   Documentation: <https://downstream.readthedocs.io>.
-->

## Installation

To install from PyPi with pip, run

`python3 -m pip install "downstream[jit]"`

A containerized release of `downstream` is available via <https://ghcr.io>

```bash
singularity exec docker://ghcr.io/mmore500/downstream:v1.11.0 python3 -m downstream --help
```

## Citing

If downstream contributes to a scientific publication, please cite it as

> Matthew Andres Moreno. (2024). mmore500/downstream. Zenodo. https://zenodo.org/doi/10.5281/zenodo.10866541

```bibtex
@software{moreno2024downstream,
  author = {Matthew Andres Moreno},
  title = {mmore500/downstream},
  month = mar,
  year = 2024,
  publisher = {Zenodo},
  doi = {10.5281/zenodo.10866541},
  url = {https://zenodo.org/doi/10.5281/zenodo.10866541}
}
```

And don't forget to leave a [star on GitHub](https://github.com/mmore500/downstream/stargazers)!
