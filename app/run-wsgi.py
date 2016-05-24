"""
Goal: Expose the `app` callable to be used by
software speaking the wsgi protocol (such as uWSGI).

@authors:
  Andrei Sura <sura.andrei@gmail.com>
"""

from olass.main import app
from olass import initializer

# Configures routes, models
app = initializer.do_init(app)
