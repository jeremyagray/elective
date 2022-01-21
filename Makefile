# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

python-modules = bin elective
python-files =

.PHONY : test-all
test-all:
	pytest -vv --cov elective --cov-report term --cov-report html

.PHONY : build
build :
	cd docs && make html
	pip install -q build
	python -m build

.PHONY : clean
clean :
	rm -rf build
	rm -rf dist
	rm -rf elective.egg-info
	cd docs && make clean

.PHONY : commit
commit :
	pre-commit run --all-files

.PHONY : dist
dist : clean build

.PHONY : docs
docs :
	cd docs && make html

.PHONY : lint
lint :
	flake8 --exit-zero $(python-modules) $(python-files)
	isort --check $(python-modules) $(python-files) || exit 0
	black --check $(python-modules) $(python-files)

.PHONY : lint-fix
lint-fix :
	isort $(python-modules) $(python-files) || exit 0
	black $(python-modules) $(python-files)

.PHONY : pip
pip :
	pip install -r requirements.txt

.PHONY : test
test:
	pytest

upload:
	python3 -m twine check dist/*
	python3 -m twine upload --verbose dist/*

upload-test:
	python3 -m twine check dist/*
	python3 -m twine upload --verbose --repository testpypi dist/*

requirements.txt: poetry.lock
	./freeze.sh > $(@)
