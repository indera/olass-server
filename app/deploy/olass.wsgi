#!/usr/bin/env python

"""
Goal: Implement wsgi helper for deployment

@authors:
  Andrei Sura <sura.andrei@gmail.com>
"""

import sys
import os
import logging
logging.basicConfig(stream=sys.stderr)

print("Using interpreter: {}".format(sys.version))

app_home = '/srv/apps/olass/src/current/app'
print("Adding application path: {}".format(app_home))
sys.path.insert(0, app_home)

from olass.main import app as application
from olass import initializer

# Configures routes, models
application = initializer.do_init(application)
