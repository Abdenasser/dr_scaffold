# How to develop on this project

dr_scaffold welcomes contributions from the community.

**You need PYTHON3!**

These instructions are for linux base systems. (Linux, MacOS, BSD, etc.)

## Setting up your own fork of this repo.

- On github interface click on `Fork` button.
- Clone your fork of this repo. `git clone git@github.com:YOUR_GIT_USERNAME/dr_scaffold.git`
- Enter the directory `cd dr_scaffold`
- Add upstream repo `git remote add upstream https://github.com/Abdenasser/dr_scaffold`

## Setting up your own virtual environment

Run `make virtualenv` to create a virtual environment.
then activate it with `source .env/bin/activate`.

## Install the project in develop mode

Run `make install` to install the project dependencies from requirements.txt.

## Run the tests to ensure everything is working

Run `make test` to run the tests.

## Create a new branch to work on your contribution

Run `git checkout -b my_contribution`

## Make your changes

Edit the files using your preferred editor. (we recommend VIM or VSCode)

## Format the code

Run `make format` to format the code.

## Run the linter

Run `make lint` to run the linter.

## Test your changes

Run `make test` to run the tests.

Ensure code coverage report shows `100%` coverage, add tests to your PR.

## Write some documentation

Ensure your new changes are documented.

## Commit your changes

This project uses [conventional git commit messages](https://www.conventionalcommits.org/en/v1.0.0/).

Example: `fix(package): update setup.py arguments 🎉` (emojis are fine too)

## Push your changes to your fork

Run `git push origin my_contribution`

## Submit a pull request

On github interface, click on `Pull Request` button.

Wait CI to run and one of the developers will review your PR.

## Makefile utilities

This project comes with a `Makefile` that contains a number of useful utility.

```bash
❯ make
Usage: make <target>

Targets:
help:             ## Show the help.
lint:             ## Run pep8, black, mypy linters.
format:           ## Format code using autoflake black & isort.
test: lint        ## Run tests and generate coverage report.
virtualenv:       ## Create a virtual environment.
install:          ## Install the project in dev mode.
```
