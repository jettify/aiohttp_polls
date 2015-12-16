aiohttp_polls
=============

Example of aiohttp polls project, similar to django one.

Create database
===============

::
    sudo -u postgres psql -c "CREATE USER aiohttp_user WITH PASSWORD 'aiohttp_user';"
    sudo -u postgres psql -c "CREATE DATABASE aiohttp_polls ENCODING 'UTF8';"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE aiohttp_polls TO aiohttp_user;"

