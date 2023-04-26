SRC_PATH := frinx
POETRY := $(shell command -v poetry 2> /dev/null)

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "  install     install packages and prepare environment"
	@echo "  venv     	 activate virtual environment"
	@echo "  clean       remove all temporary files"
	@echo "  check       run the code ruff checks"
	@echo ""
	@echo "  install-poetry     install packages and prepare environment"
	@echo "Check the Makefile to know exactly what each target is doing."

.PHONY: install-poetry
install-poetry:
	curl -sSL https://install.python-poetry.org | python3 -

.PHONY: install
install:
$(INSTALL_STAMP): pyproject.toml poetry.lock
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) install

.PHONY: init
init:
	$(POETRY) init

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	find . -type d -name '.pytest_cache' | xargs rm -rf {}
	find . -type d -name '__pycache__'| xargs rm -rf {}
	find . -type d -name '.mypy_cache' | xargs rm -rf {}
	find . -type d -name '.coverage' | xargs rm -rf {}
	find . -type d -name '.ruff_cache' | xargs rm -rf {}

.PHONY: check
check: $(INSTALL_STAMP)
	$(POETRY) run ruff check $(SRC_PATH) --fix
