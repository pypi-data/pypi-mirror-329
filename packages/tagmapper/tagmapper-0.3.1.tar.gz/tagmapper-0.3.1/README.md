# tagmapper-sdk [![SNYK dependency check](https://github.com/equinor/tagmapper-sdk/actions/workflows/snyk.yml/badge.svg)](https://github.com/equinor/tagmapper-sdk/actions/workflows/snyk.yml)
Prototype python package to get IMS-tag mappings for data models for separators and wells.

Authentication is done using Azure credentials and bearer tokens.


## Use
See [demo](examples/demo_separator.py). Or try the following simple code.  
```
from tagmapper import Well


w = Well("NO 30/6-E-2")  
```


## Installing
Install from pypi using pip.  
``
pip install tagmapper
``


## Developing
Clone repo and run ``poetry install`` to install dependencies.


## Testing
Run tests and check coverage using pytest-cov
``poetry run pytest --cov=tagmapper test/ --cov-report html``
