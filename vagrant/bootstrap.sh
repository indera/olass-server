#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

SHARED_FOLDER=/vagrant
APP_FOLDER=/srv/apps/olass
VENV_FOLDER=$APP_FOLDER/venv
DB_NAME=olass
DB_USER=olass

# import helper functions
. $SHARED_FOLDER/bootstrap_functions.sh

# Exit on first error
set -e

configure_base
install_utils
install_app_server
install_app
