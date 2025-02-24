# Django GraphQL App Setup

A Django management command to create apps with custom folder structures for graphql APIs.

## Installation

Install the package using pip:

```bash
pip install django-app-setup
```

Add the following to your `settings.py` file

```bash
INSTALLED_APPS = [
    ...
    "django_graphql_app_setup",
    ...
]
```

## Usage

In your project directory, run the following command:

```bash
python manage.py startgqlapp <app_name>