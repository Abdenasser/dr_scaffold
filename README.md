# drf_scaffold

**Scaffold django rest apis like a champion** ⚡

## Overview

Coming from a ruby on rails ecosystem I've been always wondering if there's a CLI we can use with Django to generate a bare minimum setup for our apps like the one we have in rails, so I started looking a django CLI that does the same but couldn't find anything that suits my needs.. so I decided to create one.

This Library should help you generate a full **Rest API App structure** using one command:

```console
$ python manage.py drf_scaffold blog Post title:charfield body:textfield author:foreignkey:Author

🎉 Your Post resource is ready 🎉
```

- **models.py** containing Models with all fields generated using CLI ⚡
- **admin.py** containing with the previous Models already registered ⚡
- **views.py** including Django Rest Framework ViewSets with all actions necessary for CRUD operations using Mixins, documented using swagger.⚡
- **urls.py** containing all needed URLs necessary for CRUD endpoints.⚡
- **serializers.py** contains Model Serializers for a bare minimum DRF setup to get started ⚡

## Totorial

Clone this repository :

```console
$ git clone https://github.com/Abdenasser/drf_scaffold.git
```

And cd into the project directory :

```console
$ cd drf_scaffold
```

Activate your virtualenv, then run:

```console
$ pip install -r requirements.txt
```

Let's now create our Api, run the commands below to generate our Author and Post scaffolds:

```console
$ python manage.py drf_scaffold blog Author name:charfield

🎉 Your Author resource is ready 🎉
```

```console
$ python manage.py drf_scaffold blog Post body:textfield author:foreignkey:Author

🎉 Your Post resource is ready 🎉
```

Now that our app has everything that we need let's add it to our INSTALLED_APPS and urls, open your `settings.py` file and add the app name like the following:

```python
INSTALLED_APPS = [
    ...,
    'blog'
]
```

Next, lets generate migrate our database through the following commands:

```console
$ python manage.py makemigrations
```

```console
$ python manage.py migrate
```

Next, open the urls.py file and add the path to our app urls:

```python
urlpatterns = [
    ...,
    path("blog/", include("blog.urls")),
]
```

Finally start your server with `python manage.py runserver` and head over to `http://127.0.0.1:8000/blog/posts/`
**don't forget to checkout your admin panel as well `http://127.0.0.1:8000/admin`**

## Installation and usage

**This library assumes that you have setup your project with Django Rest Framework. if not, please refer to this guide first : [Getting Started with DRF](https://www.django-rest-framework.org/#installation)**

Currently as we don't have a package ready to use yet, please follow the instructions below:
Clone this repository :

```console
$ git clone https://github.com/Abdenasser/drf_scaffold.git
```

And cd into the project directory :

```console
$ cd drf_scaffold
```

Copy the `drf_scaffold_core` application folder and `requirements.txt` file into your Django project.

**Inside your project directory (preferably)** create a virtual environment using the following command:

```console
$ python3 -m venv env
```

Next, Activate your newly created virtualenv by running:

```console
$ source env/bin/activate
```

install requirements:

```console
$ pip install -r requirements.txt
```

Add the application to your INSTALLED_APPS along with `rest_framework` like the following:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'drf_scaffold_core'
]
```

Enjoy!

## SUPPORTED FIELD TYPES

**We support most of django field types**

## TODO

- write some tests
