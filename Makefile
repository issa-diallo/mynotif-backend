VIRTUAL_ENV?=venv
PIP=$(VIRTUAL_ENV)/bin/pip
PIP_COMPILE=$(VIRTUAL_ENV)/bin/pip-compile
GUNICORN=$(VIRTUAL_ENV)/bin/gunicorn
PYTHON_MAJOR_VERSION=3
PYTHON_MINOR_VERSION=9
PYTHON_VERSION=$(PYTHON_MAJOR_VERSION).$(PYTHON_MINOR_VERSION)
PYTHON_WITH_VERSION=python$(PYTHON_VERSION)
PYTHON=$(VIRTUAL_ENV)/bin/python
ISORT=$(VIRTUAL_ENV)/bin/isort
FLAKE8=$(VIRTUAL_ENV)/bin/flake8
BLACK=$(VIRTUAL_ENV)/bin/black
PYTEST=$(VIRTUAL_ENV)/bin/pytest
WORKSPACE?=development
PORT?=8000
IMAGE_TAG=latest
AWS_ACCOUNT_ID=332944743618
AWS_PROFILE?=default
REGION=eu-west-3
REGISTRY=$(AWS_ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com
APP_NAME=mynotif-backend
IMAGE_NAME=$(APP_NAME)-ecr-$(WORKSPACE)
DOCKER_IMAGE=$(REGISTRY)/$(IMAGE_NAME)
SOURCES=src/


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
	$(PIP_COMPILE) --upgrade --output-file requirements.txt

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
	$(PYTHON) src/manage.py collectstatic --noinput

run/migrate: virtualenv
	$(PYTHON) src/manage.py migrate --noinput

run/dev: virtualenv
	$(PYTHON) src/manage.py runserver

run/prod:
	$(GUNICORN) --chdir src --bind 0.0.0.0:$(PORT) main.wsgi

docker/build:
	docker build --build-arg PORT=$(PORT) --tag=$(DOCKER_IMAGE):$(IMAGE_TAG) .

docker/run:
	docker run -it --publish $(PORT):$(PORT) --rm $(DOCKER_IMAGE):$(IMAGE_TAG)

docker/run/sh:
	docker run -it --rm $(DOCKER_IMAGE):$(IMAGE_TAG) sh

docker/login:
	aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com

docker/push:
	docker push $(DOCKER_IMAGE):$(IMAGE_TAG)

devops/terraform/fmt:
	terraform -chdir=terraform fmt

devops/terraform/select/%:
	terraform -chdir=terraform workspace select $* || terraform -chdir=terraform workspace new $*

devops/terraform/plan: devops/terraform/select/$(WORKSPACE)
	terraform -chdir=terraform plan

devops/terraform/apply: devops/terraform/select/$(WORKSPACE)
	terraform -chdir=terraform apply -auto-approve

devops/terraform/destroy: devops/terraform/select/$(WORKSPACE)
	terraform -chdir=terraform destroy -auto-approve
