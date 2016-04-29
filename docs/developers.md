# Developer's Documentation

## Introduction

The preliminary data flow diagram:

<pre>
+------+                                                                                 ________
|  O   |            +------------+            +-------+     +-------+                  /__________\
| ---  |    SSL     | RedHat 7.0 |   unix     |       |     |       |   sha256 IDs    |            |
|  |   |  --------> |   Nginx    | ---------> | uWSGI | --> | Flask | < =========== > |  1FL-DB    |
| / \  |   OAuth2   +------------+  socket    |       |     |  App  |    1FL-UUID     |  MySQL?    |
--------                                      +-------+     +-------+                 |            |
|  PS  |                                                                               \__________/
+------+

</pre>

Legend:

* PS - partner site. A person or a cron job running the client.
* SSL - secure socket layer protocol
* Nginx - [webserver](https://en.wikipedia.org/wiki/Nginx)
* uWSGI - [application server](http://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html)
* Flask - [framework for Python web-applications](http://flask.pocoo.org/)
* OAuth2 - [authorization protocol](https://tools.ietf.org/html/rfc6749).
    @see http://flask-oauthlib.readthedocs.org/en/latest/oauth2.html
    @see https://github.com/lepture/flask-oauthlib
    @see https://github.com/lepture/example-oauth2-server
    @see http://lepture.com/en/2013/create-oauth-server
    @see https://code.google.com/archive/p/google-api-python-client/downloads
    @see https://developers.google.com/api-client-library/python/guide/aaa_oauth
* sha256 - [hashing algorithm](https://en.wikipedia.org/wiki/SHA-2)
* UUID - [universally unique identifier](https://en.wikipedia.org/wiki/Universally_unique_identifier)
* 1FL-DB - the database where the sha256 strings are mapped to 1FL-UUID


## RedHat Setup

## Install webserver and supervisor
    $ sudo yum install nginx supervisor.noarch

    $ sudo yum install python-pip.noarch python-flake8.noarch pylint.noarch
    $ sudo pip install --upgrade pip
    $ sudo pip install virtualenv virtualenvwrapper

## Virtual Environment Creation

    $ mkdir $HOME/.virtualenvs

    Add to ~/.bashrc:
        export WORKON_HOME=$HOME/.virtualenvs
        source /path/to/this/file/virtualenvwrapper.sh

    $ source ~/.bashrc
    $ mkvirtualenv my_venv


## OAuth 2.0

The OAuth 2.0 Authorization Framework is described by
[rfc6749](https://tools.ietf.org/html/rfc6749)


     +--------+                               +---------------+
     |        |--(A)- Authorization Request ->|   Resource    |
     |        |                               |     Owner     |
     |        |<-(B)-- Authorization Grant ---|               |
     |        |                               +---------------+
     |        |
     |        |                               +---------------+
     |        |--(C)-- Authorization Grant -->| Authorization |
     | Client |                               |     Server    |
     |        |<-(D)----- Access Token -------|               |
     |        |                               +---------------+
     |        |
     |        |                               +---------------+
     |        |--(E)----- Access Token ------>|    Resource   |
     |        |                               |     Server    |
     |        |<-(F)--- Protected Resource ---|               |
     +--------+                               +---------------+
