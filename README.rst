
dr\_scaffold (Django Rest Scaffold)
===================================


.. image:: https://codecov.io/gh/Abdenasser/dr_scaffold/branch/main/graph/badge.svg?token=VLUZWSTJV2:target: https://codecov.io/gh/Abdenasser/dr_scaffold  
.. image:: https://app.travis-ci.com/Abdenasser/dr_scaffold.svg?branch=main:target: https://app.travis-ci.com/Abdenasser/dr_scaffold  
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg:target: https://opensource.org/licenses/MIT


**Scaffold django rest apis like a champion** ⚡

Overview
--------

Coming from a ruby on rails ecosystem I've been always wondering if
there's a CLI we can use with Django to generate a bare minimum setup
for our apps like the one we have in rails, so I started looking for a
django CLI that does the same but couldn't find anything that suits my
needs.. so I decided to create one.

**Checkout the video demo** : `Getting Started
with dr_scaffold <https://www.youtube.com/watch?v=RhMJf4pL90o>`_

This Library should help you generate full **Restful API Resources**
using one command:

.. code:: console

    $ python manage.py dr_scaffold blog Post title:charfield body:textfield author:foreignkey:Author

    🎉 Your RESTful Post api resource is ready 🎉

-  **models.py** containing Models with all fields generated using CLI ⚡
-  **admin.py** containing with the previous Models already registered ⚡
-  **views.py** including Django Rest Framework ViewSets with all
   actions necessary for CRUD operations using Mixins, documented using
   swagger.⚡
-  **urls.py** containing all needed URLs necessary for CRUD endpoints.⚡
-  **serializers.py** contains Model Serializers for a bare minimum DRF
   setup to get started ⚡
-  **and more ...**   

Totorial
--------

Install dr_scaffold package with the following command :

.. code:: console

    $ pip install dr-scaffold

Add dr_scaffold to your project INSTALLED_APPS:

.. code:: python

    INSTALLED_APPS = [
        ...,
        'dr_scaffold'
    ]

Let's now create our Api, run the commands below to generate our Author
and Post scaffolds:

.. code:: console

    $ python manage.py dr_scaffold blog Author name:charfield

    🎉 Your RESTful Author api resource is ready 🎉

.. code:: console

    $ python manage.py dr_scaffold blog Post body:textfield author:foreignkey:Author

    🎉 Your RESTful Post api resource is ready 🎉

Now that our app has everything that we need let's add it to our
INSTALLED\_APPS and urls, open your ``settings.py`` file and add the app
name like the following:

.. code:: python

    INSTALLED_APPS = [
        ...,
        'blog'
    ]

Next, lets migrate our database through the following commands:

.. code:: console

    $ python manage.py makemigrations

.. code:: console

    $ python manage.py migrate

Next, open the urls.py file and add the path to our app urls:

.. code:: python

    urlpatterns = [
        ...,
        path("blog/", include("blog.urls")),
    ]

Finally start your server with ``python manage.py runserver`` and head
over to ``http://127.0.0.1:8000/blog/posts/`` **don't forget to checkout
your admin panel as well ``http://127.0.0.1:8000/admin``**

Installation and usage
----------------------

**This library assumes that you have setup your project with Django Rest
Framework. if not, please refer to this guide first** : `Getting Started
with DRF <https://www.django-rest-framework.org/#installation>`_

Install dr_scaffold package :

.. code:: console

    $ pip install dr-scaffold

Add ``dr_scaffold`` to your INSTALLED\_APPS like this:

.. code:: python

    INSTALLED_APPS = [
        ...
        'dr_scaffold'
    ]

🎉🎉 Enjoy running the commands! 🎉🎉

SUPPORTED FIELD TYPES
---------------------

**We support most of django field types**

TODO
----

-  write some tests

