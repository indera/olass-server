"""
Goal: store shortcuts to common tasks

@authors:
    Andrei Sura <sura.andrei@gmail.com>

"""

# import os
import sys
from invoke import run, task
from tasks_utils import ask_yes_no, get_db_name, check_db_exists
# from invoke.exceptions import Failure
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


@task
def init_db(db_name=None):
    """ Create the database """
    db_name = db_name if db_name is not None else get_db_name()
    exists = check_db_exists(db_name)

    if exists:
        print(col.Fore.RED +
              "The database '{}' already exists "
              "(name retreived from schema/000/upgrade.sql)".format(db_name))
        sys.exit(1)

    if not ask_yes_no("Do you want to create the database '{}'?"
                      .format(db_name)):
        print(col.Fore.YELLOW + "Aborting at user request.")
        sys.exit(1)

    run('sudo mysql    < schema/000/upgrade.sql')
    run('sudo mysql {} < schema/001/upgrade.sql'.format(db_name))
    run('sudo mysql {} < schema/002/upgrade.sql'.format(db_name))
    run('sudo mysql {} < schema/002/data.sql'.format(db_name))


@task
def reset_db(db_name=None):
    """ Drop all tables, Create empty tables, and add data. """
    db_name = db_name if db_name is not None else get_db_name()

    if not ask_yes_no("Do you want to erase the '{}' database"
                      " and re-create it?".format(db_name)):
        print(col.Fore.YELLOW + "Aborting at user request.")
        sys.exit(1)

    run('sudo mysql    < schema/000/downgrade.sql')
    run('sudo mysql    < schema/000/upgrade.sql')
    run('sudo mysql {} < schema/001/upgrade.sql'.format(db_name))
    run('sudo mysql {} < schema/002/upgrade.sql'.format(db_name))
    run('sudo mysql {} < schema/002/data.sql'.format(db_name))
    print(col.Fore.GREEN + "[{}] Done.".format(STATUS_PASS))

@task
def go():
    """
    Start the web application using the WSGI webserver provided by Flask
    """
    run('python run.py')


@task
def test():
    """ Run tests """
    run('PYTHONPATH="." py.test -v --tb=short -s tests/ ')


@task
def coverage():
    """ Create coverage report """
    run('PYTHONPATH="." py.test --tb=short -s --cov olass '
        ' --cov-report term-missing --cov-report html tests/')


@task
def lint():
    # run("which pylint || sudo pip install pylint")
    run("pylint -f parseable olass | tee pylint.out")


@task
def clean():
    """
    Remove all generated files.
    """
    run('find . -type f -name "*.pyc" -print | xargs rm -f')
    run('rm -rf htmlcov/ .coverage pylint.out')


if __name__ == '__main__':
    list()
