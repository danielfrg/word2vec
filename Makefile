PWD := $(shell pwd)
S3DIR := ${PWD}/s3-data

.PHONY: build
build:  ## BUild package
	python setup.py sdist

.PHONY: upload
upload:  ## Uplaod package to pypi
	twine upload dist/*.tar.gz

.PHONY: env
env:  ## Create dev environment
	conda env create

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
