SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

PWD := $(shell pwd)
TEST_FILTER ?= ""
TEST_MARKERS ?= "not data"

first: help

.PHONY: clean
clean:  ## Clean build files
	@rm -rf build dist site htmlcov .pytest_cache .eggs
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


.PHONY: develop
develop:  ## Install package for development
	python -m pip install --no-build-isolation -e .


.PHONY: clean build
build: package  ## Build everything


.PHONY: package
package:  ## Build Python package (sdist)
	python setup.py sdist


.PHONY: check
check:  ## Check linting
	@flake8
	@isort --check-only --diff --recursive --project word2vec --section-default THIRDPARTY .
	@black --check .


.PHONY: fmt
fmt:  ## Format source
	@isort --recursive --project word2vec --section-default THIRDPARTY .
	@black .


.PHONY: upload-pypi
upload-pypi:  ## Upload package to PyPI
	twine upload dist/*.tar.gz


.PHONY: upload-test
upload-test:  ## Upload package to test PyPI
	twine upload --repository test dist/*.tar.gz


.PHONY: test
test:  ## Run tests
	pytest -k $(TEST_FILTER) -m $(TEST_MARKERS)


.PHONY: test-all
test-all:  ## Run all tests
	pytest -k $(TEST_FILTER)


.PHONY: report
report:  ## Generate coverage reports
	@coverage xml
	@coverage html

# ------------------------------------------------------------------------------
# Project specific

.PHONY: test-data
test-data:  ## Download test data
	mkdir -p $(PWD)/data \
	&& curl -o $(PWD)/data/text8.zip http://mattmahoney.net/dc/text8.zip \
	&& cd $(PWD)/data && unzip text8.zip \
	&& cd $(PWD)/data && head -c 100000 text8 > text8-small \
	&& curl -o $(PWD)/data/aclImdb_v1.tar.gz http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz \
 	&& cd $(PWD)/data && tar -xf aclImdb_v1.tar.gz


.PHONY: docker-img
docker-img:  ## Build test docker container
	docker build -t word2vec .


.PHONY: docker-run
docker-run:  ## Run docker container
	docker run -it -v $(PWD):/workdir word2vec
