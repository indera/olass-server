"""
Goal: store functions used in tasks.py

@authors:
    Andrei Sura <sura.andrei@gmail.com>

"""

import os
import sys
from invoke import run


def get_db_name():
    cmd = "grep -i 'create database' schema/000/upgrade.sql " \
        " | cut -d ' ' -f3 | tr -d  ';'"

    try:
        result = run(cmd, hide=True)
        return result.stdout.strip()
    except Exception as exc:
        print("Failed to run [{}] due: {}".format(cmd, exc))


def check_db_exists(db_name):
    cmd = "echo 'select count(*) from information_schema.SCHEMATA " \
          "WHERE SCHEMA_NAME = \"{}\"' | mysql -uroot " \
          "| sort | head -1".format(db_name)
    try:
        result = run(cmd, hide=True)
        return result.stdout.strip() == '1'
    except Exception as exc:
        print("Failed to run [{}] due: {}".format(cmd, exc))


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


def ask_yes_no(question, default="y"):
    """Ask a yes/no question via raw_input() and return the answer
    as a boolean.

    :param question: the question displayed to the user
    :param default: the default answer if the user hits <Enter>

    """
    valid = {"y": True, "n": False}

    if default is None:
        prompt = " [y/n] "
    elif default == "y":
        prompt = " [Y/n] "
    elif default == "n":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()

        if default is not None and choice == '':
            return valid[default]

        choice_letter = choice[0]

        if choice_letter in valid:
            return valid[choice_letter]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
