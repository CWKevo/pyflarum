#!/bin/bash
cd "$(dirname "$0")"

python setup.py sdist
twine upload ./dist/*
