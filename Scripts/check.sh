#!/bin/bash

export SOURCE_FILES="./dr_scaffold"

set -x

flake8 $SOURCE_FILES --ignore=E501,E722 --exclude=__init__.py
black --check --diff --target-version=py38 $SOURCE_FILES
mypy $SOURCE_FILES --no-site-packages