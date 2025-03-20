# Django Boilerplate

## Overview

Basic boiler plate for a dockerised Django application, with the following packages, libraries, and configuration:

- Docker
- **Django 5.1**, running on **Python 3.11.9** .
- Postgres Database, connected via psycopg, running **Postgres 16**.
- Custom user model, with username disabled, email set to required and basic tests.
- Django AllAuth, with urls and views manual added to easily disable / configure.
- Django Debug Toolbar
- Django Extensions
- **Tailwind CSS 4.0.3** (NPM Package)
- **Alpine JS 3.14.8** (CDN)
- Base Templates for authorised and non-authorised views.
- Core app, containing custom tags and a field_wrapper tag for form fields.
- Settings configured for environment variables, template directories, static directories.


## Local Development Setup

1. Clone the repo, and cd into it:

   ```shell
   $ git clone <repo-url>
   $ cd <path/to/repo>
   ```
2. Ensure you have docker installed, and that it is running.
3. Add environment variables for the following:
    - SECRET_KEY (Secret key used by Django)
    - DJANGO_DEBUG (set to True for development)

    For production, you'll also want to add the relevant variables for your database and email provider, which are used when DEBUG is set to False (see settings).

4. Build and start up the local server:

   ```shell
   $ docker-compose up --build
   ```
5. Apply migrations to the database:

    ```shell
    $ docker-compose exec web python manage.py migrate
    ```
6. Create superuser:

    ```shell
    $ docker-compose exec web python manage.py createsuperuser
    ```
7. Navigate to http://127.0.0.1:8000/ in your browser.

## Tests

To run the test suite:

```shell
$ docker-compose exec web python manage.py test
```