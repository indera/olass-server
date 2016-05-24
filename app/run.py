#!/usr/bin/env python
"""
Goal: Implement the application entry point for debugging.

Note: This file is *not* used for production deployment.
    For production we use run-wsgi.py

@authors:
  Andrei Sura <sura.andrei@gmail.com>
"""

import argparse
from olass.main import app
from olass import initializer
from config import MODE_DEBUG

# Configures routes, models
app = initializer.do_init(app, mode=MODE_DEBUG)

if __name__ == "__main__":
    """ Entry point for command line execution """
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',
                        dest='port',
                        type=int,
                        default=5000,
                        help="Application port number")
    args = parser.parse_args()
    ssl_context = initializer.get_ssl_context(app)
    print("curl -skL https://localhost:{}".format(args.port))
    app.run(host='0.0.0.0', port=args.port, ssl_context=ssl_context)
