# MyNotif with Django

[![Tests](https://github.com/issa-diallo/Mynotif_backend/actions/workflows/tests.yml/badge.svg)](https://github.com/issa-diallo/Mynotif_backend/actions/workflows/tests.yml)

## URLs

- :tada: https://mynotif-api.herokuapp.com/
- :memo: https://mynotif-api.herokuapp.com/swagger/
- :memo: https://mynotif-api.herokuapp.com/redoc/
- :goal_net: https://sentry.io/organizations/andre-5t/issues/3096848907/?project=6257099

## Install
```
pip install -r requirements.txt
pip install -e .[dev]
cp .env.example .env
```

## :tada: run
```sh
python3 src/project_nursing/manage.py runserver
```

## :test_tube: test
```
pytest src/project_nursing/tests.py src/nurse/tests.py
```

### :rotating_light: linting
```sh
flake8 src/
black src/
```

### Requirements bump
```sh
pip-compile > requirements.txt
```
The project has automated handling of production requirements, the idea behind it is that
you should always use the latest versions of every requirement.
`pip-compile` is used to handle it.

It's still possible to bump a specific version of a library, to do so:

* Place the needed fixed version using pip notation in the `setup.cfg` file
* Put a comment over the fixed requirement explaining the reason for fixing it (usually with a link to an issue/bug)
* Run `pip-compile > requirements.txt`

### DEBUG
```sh
import pdb; pdb.set_trace()
```

## Learn More

You can learn more in the api rest framework(https://www.django-rest-framework.org/) 

You can learn more build API(https://insomnia.rest/)

You can learn more in django(https://www.djangoproject.com/)
