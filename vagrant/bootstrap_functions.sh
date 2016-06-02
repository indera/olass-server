#!/bin/bash

function configure_base() {
   # Use local time so we don't have to do math when looking thru logs
   echo "US/Eastern" > /etc/timezone
   dpkg-reconfigure tzdata

   # Update packages
   apt-get update -y
}

function install_utils() {
   cp $SHARED_FOLDER/dot_files/aliases /home/vagrant/.bash_aliases
   cp $SHARED_FOLDER/dot_files/aliases /root/.bash_aliases

   cp $SHARED_FOLDER/dot_files/vimrc /home/vagrant/.vimrc
   cp $SHARED_FOLDER/dot_files/vimrc /root/.vimrc

   cp $SHARED_FOLDER/dot_files/sqliterc /home/vagrant/.sqliterc
   cp $SHARED_FOLDER/dot_files/sqliterc /root/.sqliterc

   apt-get install -y vim ack-grep nmap
}

function install_app_server() {
    apt-get install -y libssl-dev
    apt-get install -y libffi-dev libsqlite3-dev
    apt-get install -y nginx supervisor
    apt-get install -y mysql-server libmysqlclient-dev
    apt-get install -y python-pip python-dev
    apt-get install -y python-flake8 pylint
    apt-get install -y virtualenv virtualenvwrapper
}

function install_app() {
    mkdir -p $APP_FOLDER/deploy

    pushd $APP_FOLDER
        # Setting up a virtual environment will keep the application and its
        # dependencies isolated from the main system.

        log "Creating virtual environment: $VENV_FOLDER"
        virtualenv -p /usr/bin/python3 $VENV_FOLDER
        . $VENV_FOLDER/bin/activate
            log "Installing required python packages..."
            ls -al
            pip install -r /srv/apps/olass/app/requirements.txt
        deactivate
    popd

    pushd $APP_FOLDER/deploy
        log "Link app config file to make it visible in config.py... "
        # ln -sfv sample.vagrant.settings.conf settings.conf
    popd

    pushd $APP_FOLDER
        log "Creating database and tables..."

        if [ -d /var/lib/mysql/$DB_NAME ]; then
            log "Database $DB_NAME already exists... removing"
            mysql < db/000/downgrade.sql
        fi

        log "Execute sql: db/000/upgrade.sql"
        mysql -u root < db/000/upgrade.sql
        log "Execute sql: db/001/upgrade.sql"
        mysql -u root $DB_NAME   < db/001/upgrade.sql
        log "Execute sql: db/002/upgrade.sql"
        mysql -u root $DB_NAME   < db/002/upgrade.sql
        log "Execute sql: db/002/data.sql"
        mysql -u root $DB_NAME   < db/002/data.sql

        log "Execute sql: db/003/upgrade.sql"
        mysql -u root $DB_NAME   < db/003/upgrade.sql
        log "Execute sql: db/003/data.sql"
        mysql -u root $DB_NAME   < db/003/data.sql

        log "Stop the server in order to disable the default site"
        service nginx stop
        supervisorctl stop all

        log "Link config files for nginx"
        ln -sfv $APP_FOLDER/deploy/nginx-olass.conf /etc/nginx/sites-available.conf
        ln -sfv $APP_FOLDER/deploy/nginx-olass.conf /etc/nginx/sites-enabled.conf

        log "Restaring the server with new config..."
        sleep 2
        service nginx start
        supervisorctl start all

        #log "Activate the python wsgi app"
        #touch -af /srv/apps/olass/vagrant.wsgi
        #curl -sk https://localhost | grep -i 'olass'
    popd
}

function log() {
    echo -n "Log: "
    echo $*
}
