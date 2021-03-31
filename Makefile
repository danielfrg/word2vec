SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

TEST_FILTER ?= ""
TEST_MARKERS ?= "not data"


first: help


# ------------------------------------------------------------------------------
# Build

env:  ## Create Python env
	mamba env create


develop:  ## Install package for development
	python -m pip install --no-build-isolation -e .


build:  ## Build package
	python setup.py sdist


upload-pypi:  ## Upload package to PyPI
	twine upload dist/*.tar.gz


upload-test:  ## Upload package to test PyPI
	twine upload --repository test dist/*.tar.gz


# ------------------------------------------------------------------------------
# Testing

check:  ## Check linting
	flake8
	isort . --project word2vec --check-only --diff
	black . --check


fmt:  ## Format source
	isort . --project word2vec
	black .


test:  ## Run tests
	pytest -k $(TEST_FILTER) -m "$(TEST_MARKERS)"


test-all:  ## Run all tests
	pytest -k $(TEST_FILTER)


report:  ## Generate coverage reports
	coverage xml
	coverage html


test-data:  ## Download test data
	mkdir -p $(CURDIR)/data
	curl -o $(CURDIR)/data/text8.zip http://mattmahoney.net/dc/text8.zip
	cd $(CURDIR)/data && unzip text8.zip
	cd $(CURDIR)/data && head -c 100000 text8 > text8-small
	curl -o $(CURDIR)/data/aclImdb_v1.tar.gz http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz
	cd $(CURDIR)/data && tar -xf aclImdb_v1.tar.gz


docker-img:  ## Build test docker container
	docker build -t word2vec .


docker-run:  ## Run docker container
	docker run -it -v $(CURDIR):/workdir word2vec


# ------------------------------------------------------------------------------
# Other

clean:  ## Clean build files
	rm -rf build dist site htmlcov .pytest_cache .eggs
	rm -f .coverage coverage.xml word2vec/_generated_version.py
	find . -type f -name '*.py[co]' -delete
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} +
	rm -rf data/test-output*


cleanall: clean   ## Clean everything
	rm -rf *.egg-info
	rm -rf bin data


help:  ## Show this help menu
	@grep -E '^[0-9a-zA-Z_-]+:.*?##.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"; OFS="\t\t"}; {printf "\033[36m%-30s\033[0m %s\n", $$1, ($$2==""?"":$$2)}'
