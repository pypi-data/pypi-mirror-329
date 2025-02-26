[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/NEMO-wago-interlocks?label=python)](https://www.python.org/downloads/release/python-3110/)
[![PyPI](https://img.shields.io/pypi/v/nemo-wago-interlocks?label=pypi%20version)](https://pypi.org/project/NEMO-wago-interlocks/)

# NEMO Wago Interlocks

This plugin for NEMO adds compatibility with WAGO Interlocks.

# Compatibility:

### NEMO-wago-interlocks >= 0.1.0
* NEMO >= 4.7.0
* NEMO-CE >= 1.7.0

# Installation

`pip install NEMO-wago-interlocks`

# Add NEMO WAGO interlocks

in `settings.py` add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    '...',
    'NEMO_wago_interlocks',
    '...'
]
```

# Usage
* Go to Detailed Administration and add a new Interlock Card
* Pick "WAGOModbusTCP" as the card category
* Fill in the required information
* Add a new Interlock linked to the card
* Link the interlock to a tool
