# -*- coding: utf-8 -*-
"""
Goal: implement common tasks which can be invoked with the python "Fabric" tool
@see http://docs.fabfile.org/en/latest/tutorial.html

@authors:
  Andrei Sura <sura.andrei@gmail.com>
"""

from __future__ import with_statement
from fabric.api import local, task, prefix, abort
from fabric import colors
from fabric.context_managers import settings
from fabric.contrib.console import confirm
from contextlib import contextmanager

STATUS_PASS = '✔'
STATUS_FAIL = '✗'


@task
def prep_deploy():
    """ Install required Python packages """
    local('pip install -r requirements/deploy.pip')


@task
def prep_develop():
    """ Install required Python packages for developers """
    local('pip install -r requirements/dev.pip')
    local('pip install -r requirements/tests.pip')


def get_db_name():
    with settings(warn_only=True):
        cmd = "grep -i 'create database' schema/000/upgrade.sql " \
            " | cut -d ' ' -f3 | tr -d  ';'"
        db_name = local(cmd, capture=True)
    return db_name


def check_db_exists(db_name):
    cmd = "echo 'select count(*) from information_schema.SCHEMATA " \
          "WHERE SCHEMA_NAME = \"{}\"' | mysql -uroot " \
          "| sort | head -1".format(db_name)
    result = local(cmd, capture=True)
    return result == 0


@task
def init_db(db_name=None):
    """ Create the database """
    db_name = db_name if db_name is not None else get_db_name()
    exists = check_db_exists(db_name)

    if exists:
        abort(colors.red("The database '{}' already exists".format(db_name)))

    if not confirm("Do you want to create the database '{}'?".format(db_name)):
        abort(colors.yellow("Aborting at user request."))

    local('sudo mysql    < schema/000/upgrade.sql')
    local('sudo mysql {} < schema/001/upgrade.sql'.format(db_name))
    local('sudo mysql {} < schema/002/upgrade.sql'.format(db_name))
    local('sudo mysql {} < schema/002/data.sql'.format(db_name))


@task
def reset_db(db_name=None):
    """ Drop all tables, Create empty tables, and add data. """
    db_name = db_name if db_name is not None else get_db_name()

    if not confirm("Do you want to erase the '{}' database"
                   " and re-create it?".format(db_name)):
        abort(colors.yellow("Aborting at user request."))

    local('sudo mysql    < schema/000/downgrade.sql')
    local('sudo mysql    < schema/000/upgrade.sql')
    local('sudo mysql {} < schema/001/upgrade.sql'.format(db_name))
    local('sudo mysql {} < schema/002/upgrade.sql'.format(db_name))
    local('sudo mysql {} < schema/002/data.sql'.format(db_name))


@task
def test():
    """
    Run the automated test suite using py.test
    """
    local('py.test --tb=short -s tests/')


@task
def coverage():
    """
    Run the automated test suite using py.test

    # https://pytest.org/latest/example/pythoncollection.html
    local('python setup.py nosetests')
    """
    local(
        'py.test --tb=short -s --cov olass --cov-config '
        'tests/.coveragerc --cov-report term-missing --cov-report html tests/')


@task
def lint():
    local("which pylint || sudo easy_install pylint")
    local("pylint -f parseable olass | tee pylint.out")


@task
def run():
    """
    Start the web application using the WSGI webserver provided by Flask
    """
    local('python run.py')


@task
def show_versions(url='https://localhost:5000'):
    """ display latest tag and deployed tag at a specific url
    Example: fab show_versions:url=https://xyz.com
    """
    local('git fetch --tags')

    cmd = """git tag \
        | sort -t. -k 1,1n -k 2,2n -k 3,3n \
        | tail -1"""
    last_tag = local(cmd, capture=True)

    cmd2 = 'curl -sk {}'.format(url) + """ \
        | grep Version \
        | grep -oE "[0-9.]{1,2}[0-9.]{1,2}[0-9a-z.]{1,4}" \
        | tail -1"""
    deployed_tag = local(cmd2, capture=True)

    print("\nLast tag: {}".format(colors.yellow(last_tag)))
    print("Deployed tag: {}".format(colors.yellow(deployed_tag)))

    if last_tag != deployed_tag:
        print("[{}] Tags do not match!".format(colors.red(STATUS_FAIL)))
    else:
        print("[{}] Tags do match.".format(colors.green(STATUS_PASS)))


@contextmanager
def virtualenv(venv_name):
    """ Activate a context """
    """Usage example:
    def deploy():
        with virtualenv('ha'):
            run("pip freeze > requirements.txt")
    """
    # @see so/questions/1180411/activate-a-virtualenv-via-fabric-as-deploy-user
    with prefix('source ~/.virtualenvs/'+venv_name+'/bin/activate'):
        yield


@task
def clean():
    """
    Remove generated files
    """
    local('rm -rf cover/ htmlcov/ .coverage coverage.xml nosetests.xml')
    local('rm -rf .ropeproject')
    local('find . -type f -name "*.pyc" -print | xargs rm -f')
