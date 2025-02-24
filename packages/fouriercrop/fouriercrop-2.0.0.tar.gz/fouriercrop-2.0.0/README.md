
# FourierCrop


<div align="center">

[![PyPI - Version](https://img.shields.io/pypi/v/fouriercrop.svg)](https://pypi.python.org/pypi/fouriercrop)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fouriercrop.svg)](https://pypi.python.org/pypi/fouriercrop)
[![Tests](https://github.com/cryoetools/fouriercrop/workflows/tests/badge.svg)](https://github.com/cryoetools/fouriercrop/actions?workflow=tests)
[![Codecov](https://codecov.io/gh/cryoetools/fouriercrop/branch/main/graph/badge.svg)](https://codecov.io/gh/cryoetools/fouriercrop)
[![Read the Docs](https://readthedocs.org/projects/fouriercrop/badge/)](https://fouriercrop.readthedocs.io/)
[![PyPI - License](https://img.shields.io/pypi/l/fouriercrop.svg)](https://pypi.python.org/pypi/fouriercrop)

[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://www.contributor-covenant.org/version/2/1/code_of_conduct/)

</div>


FourierCrop is a Python package that enables downsampling and other operations using Fourier domain cropping techniques. These operations can be used for tasks like reducing resolution or resizing while maintaining spatial coherence.


* GitHub repo: <https://github.com/cryoetools/fouriercrop.git>
* Documentation: <https://fouriercrop.readthedocs.io>
* Free software: Apache Software License 2.0


## Features

- **FFT-based downsampling**: Performs cropping in the frequency domain to achieve efficient resizing.
- **Flexible padding options**: Allows for center cropping, padding, or combination of both.
- **Multidimensional support**: Efficiently handles 2D image or 3D volumetric data.

## Quickstart

```bash
conda create -n fouriercrop python=3.10.13 -y
conda activate fouriercrop
pip install -U fouriercrop
conda install -c conda-forge tk=*=xft_* -y
```

## Credits

This package was created with [Cookiecutter][cookiecutter] and the [fedejaure/cookiecutter-modern-pypackage][cookiecutter-modern-pypackage] project template.

[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[cookiecutter-modern-pypackage]: https://github.com/fedejaure/cookiecutter-modern-pypackage
