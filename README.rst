.. raw:: html

    <p align="center"><a href="https://github.com/Abdenasser/dr_scaffold"><img src="https://ph-files.imgix.net/99f3cc0a-58b1-4c16-bb41-1963b0a692fc.png" alt="dr_scaffold blueprint icon" height="80"/></a></p>
    <h1 align="center">dr_scaffold</h1>
    <p align="center">Scaffold django rest apis like a champion ⚡. said no one before</p>

    <p align="center">
        <a href="https://codecov.io/gh/Abdenasser/dr_scaffold"><img src="https://codecov.io/gh/Abdenasser/dr_scaffold/branch/main/graph/badge.svg?token=VLUZWSTJV2"/></a> <a href="https://app.travis-ci.com/Abdenasser/dr_scaffold"><img src="https://app.travis-ci.com/Abdenasser/dr_scaffold.svg?branch=main"/></a> <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/pypi/l/ansicolortags.svg"/></a> <a href="https://pypi.org/project/dr-scaffold/"><img src="https://d25lcipzij17d.cloudfront.net/badge.svg?id=py&r=r&type=6e&v=1.0.1&x2=0"/></a>
    </p> 
Overview
--------

Coming from a ruby on rails ecosystem I've been always wondering if
there's a CLI we can use with Django to generate a bare minimum setup
for our apps like the one we have in rails, so I started looking for a
django CLI that does the same but couldn't find anything that suits my
needs.. so I decided to create one.

**Checkout the the detailed tutorial here** : `Getting Started
with dr_scaffold <https://www.abdenasser.com/scaffold-django-apis>`_

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
.. raw:: html
   </br></br>

Tutorial
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

Let's now create our blog Api, first generate an Author:

.. code:: console

    $ python manage.py dr_scaffold blog Author name:charfield

    🎉 Your RESTful Author api resource is ready 🎉

Then a Post that's related to Author through a foreignkey:

.. code:: console

    $ python manage.py dr_scaffold blog Post body:textfield author:foreignkey:Author

    🎉 Your RESTful Post api resource is ready 🎉

Let's add our blog to INSTALLED\_APPS like the following:

.. code:: python

    INSTALLED_APPS = [
        ...,
        'blog'
    ]

Next, lets make the migrations with:

.. code:: console

    $ python manage.py makemigrations
    
Then migrate with:

.. code:: console

    $ python manage.py migrate

Now, open urls.py and add the path to our blog urls:

.. code:: python

    urlpatterns = [
        ...,
        path("blog/", include("blog.urls")),
    ]

Finally start your server with ``python manage.py runserver`` and head
over to ``http://127.0.0.1:8000/blog/posts/`` don't forget to checkout
the admin panel as well!

.. raw:: html
   </br></br>

Installation and usage
----------------------

This library assumes that you have setup your project with **Django Rest
Framework**.
if not, please refer to `this guide <https://www.django-rest-framework.org/#installation>`_

Install dr_scaffold package :

.. code:: console

    $ pip install dr-scaffold

Add ``dr_scaffold`` to your INSTALLED\_APPS like this:

.. code:: python

    INSTALLED_APPS = [
        ...
        'dr_scaffold'
    ]

Enjoy running the commands!

.. raw:: html
   </br></br>

Supported field types
---------------------

**We support most of django field types**

TODO
----

-  create a landing page
-  handle DRF ViewSets using Mixins

