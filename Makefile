SHELL := /bin/bash
.PHONY: help version bump setup docs lint test data_processing forecast_model

VERSION	= v$(shell cat pyproject.toml | grep "^version = \"*\"" | cut -d'"' -f2)

help:			## show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

version:		## display the current version
	@echo "${VERSION}"

bump: 		# bump the version
	. venv/bin/activate \
		&& poetry version patch

setup:		## setup a dev environment
	# create new python environment
	python3.11 -m venv venv
	. venv/bin/activate \
		&& pip install --upgrade poetry pre-commit \
		&& poetry install \
		&& pre-commit install

docs:	## create html documentation for the project
	. venv/bin/activate \
		&& $(MAKE) -C docs html

lint:	## lint the code
	. venv/bin/activate && black --check .
	. venv/bin/activate && flake8 .

test:			## run tests
	. venv/bin/activate \
		&& python -m pytest tests

data_processing:	## run the data processing pipeline
	. venv/bin/activate \
	    && python abc_core/run.py \
			--pipeline data_processing \
			--config configs/run_details.yml \
			--config configs/pipelines.yml \
			--config configs/directory.yml \
			--config configs/data_processing.yml \
			--config configs/forecast_model.yml \
			--raw-data-version testing \
			--processed-data-version testing

forecast_model:	## run the forecast pipeline
	. venv/bin/activate \
		&& python abc_core/run.py
			--pipeline forecast_model \
			--config configs/run_details.yml \
			--config configs/pipelines.yml \
			--config configs/directory.yml \
			--config configs/data_processing.yml \
			--config configs/forecast_model.yml \
			--processed-data-version testing \
			--run-version testing


requirements.txt: pyproject.toml	## recipe for refreshing requirements.txt from pyproject.toml
	@echo "# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT EDIT." > requirements.txt
	@echo "./" >> requirements.txt
	poetry export --without-hashes >> requirements.txt
