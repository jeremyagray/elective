# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

.PHONY : build clean commit dist docs freeze lint pip test test-all upload upload-test

test-all:
	pytest -vv --cov elective --cov-report term --cov-report html

build :
	cd docs && make html
	pip install -q build
	python -m build

clean :
	rm -rf build
	rm -rf dist
	rm -rf elective.egg-info
	cd docs && make clean

dist : clean build

docs :
	cd docs && make html

commit :
	pre-commit run --all-files

lint :
	flake8 --exit-zero
	black --check .

pip :
	pip install -r requirements.txt

freeze : requirements.txt
	pip freeze > requirements.txt

test:
	pytest --cov elective --cov-report term

upload:
	python3 -m twine check dist/*
	python3 -m twine upload --verbose dist/*

upload-test:
	python3 -m twine check dist/*
	python3 -m twine upload --verbose --repository testpypi dist/*
