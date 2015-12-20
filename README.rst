aiohttp_polls
=============

Example of polls project using aiohttp_, aiopg_ and aiohttp_jinja2_, similar to django one.

Instalation
===============
Clone and install this app:
::

    $ git clone git@github.com:jettify/aiohttp_polls.git
    $ cd aiohttp_polls
    $ pip install -e .

Create database for your project:
::

    sudo -u postgres psql -c "CREATE USER aiohttp_user WITH PASSWORD 'aiohttp_user';"
    sudo -u postgres psql -c "CREATE DATABASE aiohttp_polls ENCODING 'UTF8';"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE aiohttp_polls TO aiohttp_user;"

Run application
::
    $ python aiohttp_polls/main.py

Requirements
============
* aiohttp_
* aiopg_
* aiohttp_jinja2_


.. _Python: https://www.python.org
.. _aiohttp: https://github.com/KeepSafe/aiohttp
.. _aiopg: https://github.com/aio-libs/aiopg
.. _aiohttp_jinja2: https://github.com/aio-libs/aiohttp_jinja2
