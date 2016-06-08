#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

SHARED_FOLDER=/vagrant
DEPLOY_FOLDER=/srv/apps/olass
APP_FOLDER=$DEPLOY_FOLDER/app
SCHEMA_FOLDER=$DEPLOY_FOLDER/app/schema

VENV_FOLDER=$DEPLOY_FOLDER/venv
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
