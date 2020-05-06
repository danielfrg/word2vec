SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

TEST_FILTER ?= ""
PWD := $(shell pwd)


first: help

.PHONY: clean
clean:  ## Clean build files
	@rm -rf build dist site htmlcov .pytest_cache
	@rm -f .coverage coverage.xml word2vec/_generated_version.py
	@find . -type f -name '*.py[co]' -delete
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type d -name .ipynb_checkpoints -exec rm -rf {} +
	@rm -rf data/test-output*


.PHONY: cleanall
cleanall: clean   ## Clean everything
	@rm -rf *.egg-info
	@rm -rf bin data


.PHONY: help
help:  ## Show this help menu
	@grep -E '^[0-9a-zA-Z_-]+:.*?##.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"; OFS="\t\t"}; {printf "\033[36m%-30s\033[0m %s\n", $$1, ($$2==""?"":$$2)}'


# ------------------------------------------------------------------------------
# Package build, test and docs

.PHONY: env  ## Create dev environment
env:
	conda env create


develop:  ## Install package for development
	python -m pip install --no-build-isolation -e .


.PHONY: build
build: package  ## Build everything


.PHONY: package
package:  ## Build Python package (sdist)
	python setup.py sdist


.PHONY: check
check:  ## Check linting
	# @flake8 word2vec
	@isort --check-only --diff --recursive --project word2vec --section-default THIRDPARTY word2vec .
	@black --check word2vec .


.PHONY: fmt
fmt:  ## Format source
	@isort --recursive --project word2vec --section-default THIRDPARTY word2vec .
	@black word2vec .


.PHONY: upload-pypi
upload-pypi:  ## Upload package to PyPI
	twine upload dist/*.tar.gz


.PHONY: upload-test
upload-test:  ## Upload package to test PyPI
	twine upload --repository testpypi dist/*.tar.gz


.PHONY: test
test:  ## Run tests
	pytest -s -vv word2vec/tests -k $(TEST_FILTER)

# ------------------------------------------------------------------------------
# Project specific

.PHONY: test-data
test-data:  ## Download test data
	mkdir -p $(PWD)/data \
	&& curl -o $(PWD)/data/text8.zip http://mattmahoney.net/dc/text8.zip \
	&& cd $(PWD)/data && unzip text8.zip \
	&& cd $(PWD)/data && head -c 10000 text8 > text8-small
