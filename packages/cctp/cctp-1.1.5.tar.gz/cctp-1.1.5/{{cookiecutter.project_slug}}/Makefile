FIND_NAME = find . -path './.venv' -prune -o -name

.PHONY: bump clean clean-build clean-pyc clean-test coverage dist doc help init install lint publish sync view

.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"
COVERAGE := .venv\Scripts\python -m coverage
SPHINX := .venv\Scripts\python -m sphinx
SPHINX_APIDOC := .venv\Scripts\sphinx-apidoc
SPHINX_BUILD := .venv\Scripts\sphinx-build
WATCHMEDO := uvx --from watchdog watchmedo

bump: ## bump project version using `bump-my-version`
	uvx --from bump2version bumpversion patch

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	$(FIND_NAME) '*.egg-info' -exec rm -fr {} +
	$(FIND_NAME) '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	$(FIND_NAME) '*.pyc' -exec rm -f {} +
	$(FIND_NAME) '*.pyo' -exec rm -f {} +
	$(FIND_NAME) '*~' -exec rm -f {} +
	$(FIND_NAME) '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

coverage: sync ## check code coverage quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	$(COVERAGE) run --source {{ cookiecutter.project_slug }} -m pytest
{%- else %}
	$(COVERAGE) run --source {{ cookiecutter.project_slug }} setup.py test
{%- endif %}
	$(COVERAGE) report -m
	$(COVERAGE) html
	$(BROWSER) htmlcov/index.html

doc: sync ## generate Sphinx HTML documentation, including API docs
	rm -f docs/{{ cookiecutter.project_slug }}.rst
	rm -f docs/modules.rst
	$(SPHINX_APIDOC) -o docs/ src/{{ cookiecutter.project_slug }}
	rm -rf docs/_build
	$(SPHINX_BUILD) docs docs/_build
	$(BROWSER) docs/_build/index.html

dist: clean ## builds source and wheel package
	uv build
	ls -l dist

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

init: clean sync ## initialize environment
	git init
	.venv\Scripts\activate
	.venv\Scripts\pre-commit install

install: clean sync ## install the package to the active Python's site-packages

lint: sync ## check style with ruff
	.venv\Scripts\ruff check src tests --fix

publish: dist ## publish to pypi
	uv build
	uv publish

servedoc: sync docs ## compile the docs watching for changes
	$(WATCHMEDO) shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

sync: ## sync project using uv
	uv sync

test: sync ## run tests quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	.venv\Scripts\python -m pytest
{%- else %}
	.venv\Scripts\python -m unittest
{%- endif %}

test-all: ## run tests on every Python version with tox
	.venv\Scripts\tox

view: ## view HTML documentation, including API docs
	$(BROWSER) docs/_build/index.html
