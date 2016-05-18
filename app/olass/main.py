"""
Goal: Init the Flask Singletons 'app' and 'db' used by ../run.py

@authors:
  Andrei Sura <sura.andrei@gmail.com>
"""

try:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
except ImportError as error:
    import sys
    sys.exit("Missing required package: {}".format(error))


# The WSGI compliant web-application object
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# The Object-Relationan-Mapping (ORM) object
db = SQLAlchemy(app)
