#!/bin/bash -e

export SOURCE_FILES="./dr_scaffold"

set -x

autoflake --remove-all-unused-imports --in-place --recursive $SOURCE_FILES --exclude=__init__.py
isort $SOURCE_FILES
black --target-version=py38 $SOURCE_FILES