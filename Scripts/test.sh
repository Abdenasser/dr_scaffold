#!/bin/bash -e

export SOURCE_FILES="./tests"

set -x

pytest $SOURCE_FILES --cov=dr_scaffold --cov-report=html
pytest --pylint
