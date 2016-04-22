"""
Goal: Define a generic page for the index

@authors:
  Andrei Sura <sura.andrei@gmail.com>
"""

from flask import render_template
from olass.main import app
# from olass import utils


@app.route('/', methods=['GET'])
def index():
    """ Render the index page"""
    return render_template('index.html')
