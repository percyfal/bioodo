.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
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

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	flake8 bioodo tests

test: ## run tests quickly with the default Python
	py.test


test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source bioodo -m pytest

		coverage report -m
		coverage html
		$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/bioodo.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ bioodo
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html


GH_PAGES_SOURCES = docs docs/Makefile bioodo
GH_PAGES_DOCS = *.html *.inv *.js _*
gh-pages: ## generate Sphinx HTML documentation, including API docs, for gh-pages
	python setup.py version 2>/dev/null | grep Version | sed "s/Version://" > .version
	git checkout gh-pages
	rm -f docs/bioodo.rst
	rm -f docs/modules.rst
	git checkout master $(GH_PAGES_SOURCES)
	git reset HEAD
	sphinx-apidoc -o docs/ bioodo
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	rsync -av docs/_build/html/* ./
	rm -rf $(GH_PAGES_SOURCES) _build .version __pycache__
	git add -A -f $(GH_PAGES_DOCS)
	git commit -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`" && git push origin gh-pages ; git checkout master

gh-pages-dev: ## generate Sphinx HTML documentation, including API docs, for gh-pages-dev
	python setup.py version 2>/dev/null | grep Version | sed "s/Version://" > .version
	git checkout gh-pages
	rm -f docs/bioodo.rst
	rm -f docs/modules.rst
	git checkout develop $(GH_PAGES_SOURCES)
	git reset HEAD
	sphinx-apidoc -o docs/ bioodo
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	rsync -av docs/_build/html/* ./
	rm -rf $(GH_PAGES_SOURCES) _build .version __pycache__
	git add -A -f $(GH_PAGES_DOCS)
	git commit -m "Generated gh-pages for `git log develop -1 --pretty=short --abbrev-commit`" && git push origin gh-pages ; git checkout develop

viewdocs: gh-pages ## View documentation
	$(BROWSER) docs/_build/html/index.html	

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

conda: clean ## package and upload a conda release
	conda build conda
	anaconda upload $(shell conda build conda --output)

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
