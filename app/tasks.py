# -*- coding: utf-8 -*-
"""
Goal: store shortcuts to common tasks

@authors:
    Andrei Sura <sura.andrei@gmail.com>

"""

import os
import sys
from invoke import run, task
import colorama as col
# @see https://pypi.python.org/pypi/colorama
col.init(autoreset=True)

STATUS_PASS = '✔'
STATUS_FAIL = '✗'

@task
def list():
    """ Show available tasks """
    run('inv -l')


@task
def prep_develop():
    """ Install the requirements """
    run('pip install -r requirements.txt')
    print(col.Fore.GREEN + "==> Pip packages installed:")
    run('pip freeze')


def get_dir_for_prefix(prefix):
    """
    Add the current username as a sub-folder to the specified 'prefix' folder
    """
    result = run('whoami', hide='stdout')
    suffix = result.stdout.strip() if result.ok else 'whoami'
    path = os.path.join(prefix, suffix)

    if not os.path.isdir(path):
        sys.exit("Do you really intend to use path [{}]?".format(path))
    return path


@task
def test():
    """ Run tests """
    run('PYTHONPATH="." py.test -v --tb=short -s tests/ ')


@task
def coverage():
    """ Create coverage report """
    run('coverage run --source tests/ -m py.test')


@task
def clean():
    """
    Remove all generated files.
    """
    run("rm **/*.pyc")


if __name__ == '__main__':
    list()
