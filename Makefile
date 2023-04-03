# Globals
.PHONY: help local build accept
.DEFAULT: help
.ONESHELL:
.SILENT:
SHELL=/bin/bash
.SHELLFLAGS = -ceo pipefail
AIRFLOW_VERSION = 2.4.3

# Targets
PIPENV_TARGET = Python Pipenv Setup Target, also install for development
AIRFLOW_TARGET = Airflow Library Installation Target, VERSION: ${AIRFLOW_VERSION}
LINT_TARGET = Python Linting: black, flake8, mypy no-strict
ASTRO_TARGET = Astro Python Pytest Run, plus Lint
INIT_TARGET = Airflow Docker Compose Init Target
UP_TARGET = Airflow Docker Compose Up Target, http://localhost:8080
DOWN_TARGET = Airflow Docker Compose Down Target, remove containers
CLEAN_TARGET = Airflow Docker Compose Clean Target, remove images and containers

# Colours for Help Message and INFO formatting
YELLOW := "\e[1;33m"
NC := "\e[0m"
INFO := @bash -c 'printf $(YELLOW); echo "=> $$0"; printf $(NC)'
export

help:
	$(INFO) "Run: make <target>"
	$(INFO) "List of Supported Targets:"
	@echo -e "pipenv -> $$PIPENV_TARGET"
	@echo -e "airflow -> $$AIRFLOW_TARGET"
	@echo -e "lint -> $$LINT_TARGET"
	@echo -e "astro -> $$ASTRO_TARGET"	
	@echo -e "init -> $$INIT_TARGET"
	@echo -e "up -> $$UP_TARGET"
	@echo -e "down -> $$DOWN_TARGET"
	@echo -e "clean -> $$CLEAN_TARGET"	

pipenv:
	pipenv sync --dev

airflow:
	pipenv run pip install --upgrade pip
	pipenv run pip install "apache-airflow[celery]==${AIRFLOW_VERSION}" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.7.txt"

lint:
	pipenv run black .
	pipenv run flake8
	pipenv run mypy --ignore-missing-imports .

astro: lint
	astro dev parse
	astro dev pytest

init:
	$(INFO) "$$INIT_TARGET"
	docker-compose up airflow-init

up:
	$(INFO) "$$UP_TARGET"
	docker-compose up

down:
	$(INFO) "$$DOWN_TARGET"
	docker-compose down

clean:
	$(INFO) "$$CLEAN_TARGET"
	docker-compose down --volumes --rmi all
