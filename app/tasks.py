"""
Goal: store shortcuts to common tasks

@authors:
    Andrei Sura <sura.andrei@gmail.com>

"""
import sys
from invoke import task
from tasks_utils import ask_yes_no, get_db_name, check_db_exists

STATUS_PASS = '✔'
STATUS_FAIL = '✗'


@task
def list(ctx):
    """ Show available tasks """
    ctx.run('inv -l')


@task
def prep_develop(ctx):
    """ Install the requirements """
    ctx.run('pip install -r requirements.txt')
    print("==> Pip packages installed:")
    ctx.run('pip freeze')


@task
def init_db(ctx, db_name=None):
    """ Create the database """
    db_name = db_name if db_name is not None else get_db_name()
    exists = check_db_exists(db_name)

    if exists:
        print("The database '{}' already exists "
              "(name retrieved from schema/000/upgrade.sql)".format(db_name))
        sys.exit(1)

    if not ask_yes_no("Do you want to create the database '{}'?"
                      .format(db_name)):
        print("Aborting at user request.")
        sys.exit(1)

    ctx.run('sudo mysql    < schema/000/upgrade.sql')
    ctx.run('sudo mysql {} < schema/001/upgrade.sql'.format(db_name))
    ctx.run('sudo mysql {} < schema/002/upgrade.sql'.format(db_name))
    ctx.run('sudo mysql {} < schema/002/data.sql'.format(db_name))
    ctx.run('sudo mysql {} < schema/003/upgrade.sql'.format(db_name))
    ctx.run('sudo mysql {} < schema/003/data.sql'.format(db_name))
    print("[{}] Done.".format(STATUS_PASS))


@task
def reset_db(ctx, db_name=None):
    """ Drop all tables, Create empty tables, and add data """
    db_name = db_name if db_name is not None else get_db_name()

    if not ask_yes_no("Do you want to erase the '{}' database"
                      " and re-create it?".format(db_name)):
        print("Aborting at user request.")
        sys.exit(1)

    ctx.run('sudo mysql    < schema/000/downgrade.sql')
    ctx.run('sudo mysql    < schema/000/upgrade.sql')
    ctx.run('sudo mysql {} < schema/001/upgrade.sql'.format(db_name))
    ctx.run('sudo mysql {} < schema/002/upgrade.sql'.format(db_name))
    ctx.run('sudo mysql {} < schema/002/data.sql'.format(db_name))
    ctx.run('sudo mysql {} < schema/003/upgrade.sql'.format(db_name))
    ctx.run('sudo mysql {} < schema/003/data.sql'.format(db_name))
    print("[{}] Done.".format(STATUS_PASS))


@task(aliases=['run'])
def go(ctx):
    """
    Start the web application using the WSGI webserver provided by Flask
    """
    ctx.run('python run.py')


@task
def show_versions(ctx, url='https://localhost'):
    # run ('git fetch --tags')

    cmd = """git tag \
        | sort -t. -k 1,1n -k 2,2n -k 3,3n \
        | tail -1"""
    cmd2 = 'curl -sk {}'.format(url) + """ \
            | grep Version \
            | grep -oE "[0-9.]{1,2}[0-9.]{1,2}[0-9a-z.]{1,4}" \
            | tail -1"""

    last_tag = ctx.run(cmd, pty=False, hide='both')
    deployed_tag = ctx.run(cmd2, pty=False, hide='both')

    print("Last tag in the repository: {}".format(last_tag.stdout.strip()))
    print("Deployed tag: {}".format(deployed_tag.stdout.strip()))

    if last_tag != deployed_tag:
        print("[{}] Tags do not match!".format(STATUS_FAIL))
    else:
        print("[{}] Tags do match.".format(STATUS_PASS))


@task
def test(ctx):
    """ Run tests """
    ctx.run('PYTHONPATH="." py.test -v --tb=short -s tests/ --color=yes')


@task(aliases=['cov'])
def coverage(ctx):
    """ Create coverage report """
    ctx.run('PYTHONPATH="." py.test --tb=short -s --cov olass '
            ' --cov-report term-missing --cov-report html tests/')
    ctx.run('open htmlcov/index.html')


@task
def lint(ctx):
    ctx.run("which pylint || pip install pylint")
    ctx.run("pylint -f parseable olass")


@task
def clean(ctx):
    """
    Remove all generated files
    """
    ctx.run('find . -type f -name "*.pyc" -print | xargs rm -f')
    ctx.run('rm -rf htmlcov/ .coverage pylint.out')
    ctx.run('rm -rf .tox/*')


if __name__ == '__main__':
    list()
