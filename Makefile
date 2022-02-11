.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: lint
lint:             ## Run pep8, black, mypy linters.
	$(ENV_PREFIX)flake8 dr_scaffold/ --ignore=E501,E722 --exclude=__init__.py --exclude=dr_scaffold/scaffold_templates/
	$(ENV_PREFIX)black --check --diff dr_scaffold/
	$(ENV_PREFIX)black --check --diff tests/
	$(ENV_PREFIX)mypy --ignore-missing-imports dr_scaffold/

.PHONY: format
format:           ## Format code using autoflake black & isort.
	$(ENV_PREFIX)autoflake --remove-all-unused-imports --in-place --recursive dr_scaffold/ --exclude=__init__.py
	$(ENV_PREFIX)isort dr_scaffold/
	$(ENV_PREFIX)black dr_scaffold/
	$(ENV_PREFIX)black tests/

.PHONY: test
test:             ## Run tests and generate coverage report.
	$(ENV_PREFIX)pytest -v --cov-config .coveragerc --cov=dr_scaffold -l --tb=short --maxfail=1 tests/
	$(ENV_PREFIX)coverage xml
	$(ENV_PREFIX)coverage html

.PHONY: virtualenv
virtualenv:       ## Create a virtual environment.
	@echo "creating a virtualenv at .env ..."
	@rm -rf .env
	@python3 -m virtualenv .env
	@echo "!!! Please run 'source .env/bin/activate' to enable the environment !!!"

.PHONY: install
install:          ## Install the project in dev mode.
	@echo "installing packages from requirements.txt ..."
	@./.env/bin/pip install -r requirements.txt
