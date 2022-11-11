VIRTUAL_ENV?=venv
PIP=$(VIRTUAL_ENV)/bin/pip
PIP_COMPILE=$(VIRTUAL_ENV)/bin/pip-compile
PYTHON_MAJOR_VERSION=3
PYTHON_MINOR_VERSION=9
PYTHON_VERSION=$(PYTHON_MAJOR_VERSION).$(PYTHON_MINOR_VERSION)
PYTHON_WITH_VERSION=python$(PYTHON_VERSION)
PYTHON=$(VIRTUAL_ENV)/bin/python
ISORT=$(VIRTUAL_ENV)/bin/isort
FLAKE8=$(VIRTUAL_ENV)/bin/flake8
BLACK=$(VIRTUAL_ENV)/bin/black
PYTEST=$(VIRTUAL_ENV)/bin/pytest
PORT?=8000
SOURCES=src/
ifndef CI
DOCKER_IT=-it
endif


all: virtualenv

$(VIRTUAL_ENV):
	$(PYTHON_WITH_VERSION) -m venv $(VIRTUAL_ENV)
	$(PYTHON) -m pip install --upgrade pip setuptools

virtualenv: $(VIRTUAL_ENV)
	$(PIP) install --requirement requirements.txt

virtualenv/test: virtualenv
	$(PIP) install -e .[dev]

requirements.txt: | $(VIRTUAL_ENV)
	$(PYTHON) -m pip install --upgrade pip-tools
	$(PIP_COMPILE) --upgrade --output-file requirements.txt requirements.in

clean:
	rm -rf venv/ .pytest_cache/

unittest:
	$(PYTEST) src/main/tests.py src/nurse/tests.py

lint/isort:
	$(ISORT) --check-only --diff $(SOURCES)

lint/flake8:
	$(FLAKE8) $(SOURCES)

lint/black:
	$(BLACK) --check $(SOURCES)

lint: lint/isort lint/flake8 lint/black

format/isort:
	$(ISORT) $(SOURCES)

format/black:
	$(BLACK) $(SOURCES)

format: format/isort format/black

test: unittest lint

run/collectstatic: virtualenv
	$(PYTHON) manage.py collectstatic --noinput

run/migrate: virtualenv
	$(PYTHON) manage.py migrate --noinput

run/dev: virtualenv
	$(PYTHON) manage.py runserver
