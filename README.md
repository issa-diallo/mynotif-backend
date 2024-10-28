# OrdoPro backend

[![Tests](https://github.com/mynotif/mynotif-backend/actions/workflows/tests.yml/badge.svg)](https://github.com/mynotif/mynotif-backend/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/mynotif/mynotif-backend/graph/badge.svg?token=RPS12B9119)](https://codecov.io/github/mynotif/mynotif-backend)
[![Deployment](https://github.com/mynotif/mynotif-backend/actions/workflows/deployment.yml/badge.svg)](https://github.com/mynotif/mynotif-backend/actions/workflows/deployment.yml)

## URLs

- :tada: https://api.ordopro.fr/
- :memo: https://api.ordopro.fr/swagger/
- :memo: https://api.ordopro.fr/redoc/
- :goal_net: https://andre-5t.sentry.io/issues/?project=6257099

## Install

```sh
make virtualenv/test
cp .env.example .env
```

## :tada: run

```sh
make run/dev
```

## :test_tube: test

```sh
make unittest
```

## :rotating_light: linting

```sh
make lint
make format
```

## Requirements bump

```sh
make -B requirements.txt
```

The project has automated handling of production requirements, the idea behind it is that
you should always use the latest versions of every requirement.
`pip-compile` is used to handle it.

## Docker

```sh
make docker/build
make docker/run
```

## Terraform

Deployment:

```sh
AWS_PROFILE=<aws_profile> make devops/terraform/plan
```

## Learn More

You can learn more in the api rest framework(https://www.django-rest-framework.org/)

You can learn more build API(https://insomnia.rest/)

You can learn more in django(https://www.djangoproject.com/)
