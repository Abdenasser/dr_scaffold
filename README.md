# drf_scaffold

**Scaffold django rest apis like a champion** ⚡

## Overview

Coming from a ruby on rails ecosystem I've been always wondering if there's a CLI we can use with Django to generate a bare minimum setup for our apps like the one we have in rails and that we can use to generate Models, Views, Controllers... and even a resource scaffold that contains all of them, so I started looking and experimenting a few small libraries here and there but most of them if not all either outdated or buggy and doesn't do the job.. so I decided to create mine but for Django rest apis.

This Library should help you generate a full **Rest API App structure** using one command:

```
python manage.py drf_scaffold blog Post title:charfield body:textfield author:foreignkey:Author
```

- **models.py** containing Models with all fields generated using CLI ⚡
- **views.py** including Django Rest Framework ViewSets with all actions necessary for CRUD operations using Mixins, documented using swagger.⚡
- **urls.py** containing all needed URLs necessary for CRUD endpoints.⚡
- **serializers.py** contains Model Serializers for a bare minimum DRF setup to get started ⚡

## Installation and usage

⚠️ **This library assumes that you have setup your project with Django Rest Framework. if not, please refer to this guide first : [Getting Started with DRF](https://www.django-rest-framework.org/#installation)**

Currently as we don't have a package ready to use yet, please follow the instructions below:
Clone this repository :

```
git clone https://github.com/Abdenasser/drf_scaffold.git
```

And cd into the project directory :

```
cd drf_scaffold
```

Copy the `drf_scaffold` application folder (not the project folder) into your Django project.
Add the application to your INSTALLED_APPS like the following:

```
INSTALLED_APPS = [
    ...
    'drf_scaffold'
]

```

Enjoy running the CLI command as follow :

```
python manage.py drf_scaffold apps_folder_name/app_name Article title:charfield body:textfield author:foreignkey:Author category:foreignkey:Category
```

don't forget to add the generated application to your INSTALLED_APPS.

## TODO

- most importantly Implement views, urls, serializers.
