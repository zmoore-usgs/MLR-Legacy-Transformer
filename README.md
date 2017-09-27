# MLR-Legacy-Transformer
[![Build Status](https://travis-ci.org/USGS-CIDA/MLR-Legacy-Transformer.svg?branch=master)](https://travis-ci.org/USGS-CIDA/MLR-Legacy-Transformer)
[![Coverage Status](https://coveralls.io/repos/github/USGS-CIDA/MLR-Legacy-Transformer/badge.svg)](https://coveralls.io/github/USGS-CIDA/MLR-Legacy-Transformer)

Provides services to transform legacy data fields

This project has been built and tested with python 3.6.x. To build the project locally you will need
python 3 and virtualenv installed.
```bash
% virtualenv --python=python3 env
% env/bin/pip install -r requirements.txt
```
To run the tests:
```bash
env/bin/python -m unittest
```

To run the application locally execute the following:
```bash
% env/bin/python app.py
```

The swagger documentation can then be accessed at http://127.0.0.1:5000/api

Default configuration variables can be overridden be creating a .env file. For instance to turn debug on, 
you will want to create an .env with the following:
```python
DEBUG = True