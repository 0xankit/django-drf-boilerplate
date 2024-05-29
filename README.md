# Django DRF template

This is a Django DRF template with a simple user model and JWT authentication.

## Features

 - [ ] Password based authentication
 - [ ] Role based authroization
 - [ ] Structured Logging
 - [ ] translation
 - [ ] Custom user model
 - [ ] DB support for Postgres
 - [ ] Docker support
 - [ ] Swagger documentation
 - [ ] Custom permission classes
 - [ ] Custom group based permission classes
 - [ ] Custom throttling classes
 - [ ] Django signals
 - [ ] Django cache
 - [ ] DB routers
 - [ ] Tests
 - [ ] Structured api response
 - [ ] DB seeding

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install the dependencies
4. Run the server

## Usage

1. Generate translation files: `python manage.py makemessages -l en_IN`
2. `django-admin compilemessages`
3. ```bash
    python manage.py makemigrations users
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
   ```


## Common commands
1. Check for errors: `python manage.py check`
2. Create superuser: `python manage.py createsuperuser`
3. Run the server: `python manage.py runserver`
4. Run tests: `python manage.py test`
5. Run tests with coverage: `coverage run --source='.' manage.py test && coverage report`
6. Generate translation files: `python manage.py makemessages -l en_IN`
7. Compile translation files: `django-admin compilemessages`
8. Generate migration files: `python manage.py makemigrations`
9. Migration: `python manage.py migrate`
10. 
