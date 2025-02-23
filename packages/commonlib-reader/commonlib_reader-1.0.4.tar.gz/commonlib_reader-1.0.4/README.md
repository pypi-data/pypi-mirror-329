# commonlib-reader [![SNYK dependency check](https://github.com/equinor/commonlib-reader/actions/workflows/snyk.yml/badge.svg)](https://github.com/equinor/commonlib-reader/actions/workflows/snyk.yml)
Connector package for Equinor Commonlib api. Used for getting code tables.

Some additional functionality for asset specific Tag categories and tag types is also included.

## Use
Try it out by running the [demo](examples/demo.py).

## Installing

Install package from pypi using `pip install commonlib_reader`


## Developing / testing

Poetry is preferred for developers. Clone and install with required packages for testing and coverage:  
`poetry install`

For testing with coverage run:  
`poetry run pytest --cov --cov-report=html`
