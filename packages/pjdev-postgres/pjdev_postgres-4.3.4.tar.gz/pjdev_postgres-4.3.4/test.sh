#!/bin/bash

export PYTHONPATH=./src:./tests
#coverage run -m pytest tests
pytest tests/*.py -vv
