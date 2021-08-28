help:
	@echo "scripts:"
	@echo "    make check:     check code quality using flake8 and black"
	@echo "    make format:     code format with autoflake, isort and black"
	@echo "    make test:     run tests and pylint"

check:
	./scripts/check.sh

format:
	./scripts/format.sh

test:
	./scripts/test.sh

