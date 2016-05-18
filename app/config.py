"""
Goal: Implement the default-config and test-config clases

@authors:
    Andrei Sura <sura.andrei@gmail.com>
"""

import os
from datetime import timedelta
import logging

BASEDIR = os.path.abspath(os.path.dirname(__file__))

MODE_TEST = 'mode_test'     # for unit tests
MODE_PROD = 'mode_prod'     # for production
MODE_DEBUG = 'mode_debug'   # for developer mode


class DefaultConfig(object):
    """ Implement the "Default configuration" class.
    Note: we pass the 'mode' paramter to
        initializer.py#do_init() choose the "config" class.
    """
    LOG_LEVEL = logging.INFO

    # When we deploy we use /srv/apps/olass/ folder
    CONFIDENTIAL_SETTINGS_FILE = os.path.join(BASEDIR,
                                              '/srv/apps/olass/settings.py')

    # SSL Certificate config
    # Note: the paths to the certificate do *not matter* when the app is
    # served by Apache since Apache has its own configuration for that
    SERVER_SSL_KEY_FILE = 'ssl/server.key'
    SERVER_SSL_CRT_FILE = 'ssl/server.crt'

    # the browser will not send a cookie with the secure flag set over an
    # unencrypted HTTP request
    SESSION_COOKIE_SECURE = True

    # https://www.owasp.org/index.php/Session_Management_Cheat_Sheet
    # flask.pocoo.org/docs/0.10/api/#flask.Flask.permanent_session_lifetime
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    DEBUG = False
    TESTING = False

    DEBUG_TB_ENABLED = False

    # Set to True in order to view every redirect in the debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Limit the max upload size for the app to 20 MB
    # @see https://pythonhosted.org/Flask-Uploads/
    DEFAULT_MAX_CONTENT_LENGTH = 20 * 1024 * 1024
    MAX_CONTENT_LENGTH = DEFAULT_MAX_CONTENT_LENGTH

    # THREADS_PER_PAGE = 8
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = ""


class DebugConfig(DefaultConfig):
    """
    Extend the default config with options useful during debugging.

    Note: the options in CONFIDENTIAL_SETTINGS_FILE
           will override what we set in this method.
    """
    LOG_LEVEL = logging.DEBUG
    DEBUG = True
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CONFIDENTIAL_SETTINGS_FILE = os.path.join(BASEDIR, 'deploy/settings.py')


class TestConfig(DefaultConfig):
    """ Configuration for running tests """
    # PRESERVE_CONTEXT_ON_EXCEPTION = False
    TESTING = True
    CSRF_ENABLED = False
    CONFIDENTIAL_SETTINGS_FILE = os.path.join(BASEDIR,
                                              'deploy/settings.py')

    if os.getenv('CONTINUOUS_INTEGRATION', '') > '':
        print("CONTINUOUS_INTEGRATION: {}"
              .format(os.getenv('TRAVIS_BUILD_DIR')))
