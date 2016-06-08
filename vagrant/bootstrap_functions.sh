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

    apt-get install -y nginx supervisor uwsgi-plugin-python3

    # Run uwsgi under nginx group
    adduser --system --no-create-home --disabled-login --disabled-password --group nginx
    adduser --system --no-create-home --disabled-login --disabled-password --ingroup nginx uwsgi

    apt-get install -y mysql-server libmysqlclient-dev
    apt-get install -y python-pip python-dev
    apt-get install -y python3-dev

    apt-get install -y python-flake8 pylint
    apt-get install -y virtualenv virtualenvwrapper

    # Get the proper uWSGI - uwsgi-2.0.13.1.tar.gz
    wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py
    rm get-pip.py
    pip3 install uwsgi uwsgitop
    apt-get install -y uwsgi-plugin-python3
    uwsgi --plugins-list
}

function install_app() {
    pushd $DEPLOY_FOLDER
        # Setting up a virtual environment will keep the application and its
        # dependencies isolated from the main system.

        log "Creating virtual environment: $VENV_FOLDER"
        virtualenv -p /usr/bin/python3 $VENV_FOLDER
        . $VENV_FOLDER/bin/activate
            log "Installing required python packages..."
            ls -al
            pip install -r $APP_FOLDER/requirements.txt
        deactivate
    popd

    pushd $DEPLOY_FOLDER
        log "Link app config file to make it visible in config.py... "
        ln -sfv $DEPLOY_FOLDER/app/deploy/vagrant-settings.conf settings.conf
    popd

    pushd $APP_FOLDER
        log "Creating database and tables..."

        if [ -d /var/lib/mysql/$DB_NAME ]; then
            log "Database $DB_NAME already exists... removing"
            mysql < $SCHEMA_FOLDER/000/downgrade.sql
        fi

        log "Execute sql: 000/upgrade.sql"
        mysql -u root < $SCHEMA_FOLDER/000/upgrade.sql
        log "Execute sql: 001/upgrade.sql"
        mysql -u root $DB_NAME   < $SCHEMA_FOLDER/001/upgrade.sql
        log "Execute sql: 002/upgrade.sql"
        mysql -u root $DB_NAME   < $SCHEMA_FOLDER/002/upgrade.sql
        log "Execute sql: 002/data.sql"
        mysql -u root $DB_NAME   < $SCHEMA_FOLDER/002/data.sql

        log "Execute sql: 003/upgrade.sql"
        mysql -u root $DB_NAME   < $SCHEMA_FOLDER/003/upgrade.sql
        log "Execute sql: 003/data.sql"
        mysql -u root $DB_NAME   < $SCHEMA_FOLDER/003/data.sql


        # Stop the supervisor to modify the config
        supervisorctl stop all

        # Link the supervisor config file to manage the process:
        #   uwsgi /srv/apps/olass/app/deploy/vagrant-uwsgi.ini
        ln -sfv /srv/apps/olass/app/deploy/vagrant-supervisord.conf /etc/supervisor/conf.d/vagrant-supervisord.conf
        supervisorctl reread
        supervisorctl start all

        log "Stop Nginx to disable the default site"
        service nginx stop

        log "Remove default site: /etc/nginx/sites-enabled/default"
        rm -f /etc/nginx/sites-enabled/default

        # Download the siteman
        wget -q -O /usr/local/sbin/siteman https://raw.githubusercontent.com/indera/siteman/master/siteman
        chmod +x /usr/local/sbin/siteman
        siteman -l

        log "Link config files for nginx"
        ln -sfv $APP_FOLDER/deploy/vagrant-nginx /etc/nginx/sites-available/vagrant-nginx
        ln -sfv /etc/nginx/sites-available/vagrant-nginx /etc/nginx/sites-enabled/vagrant-nginx
        ln -sfv $APP_FOLDER/ssl/server.crt /etc/ssl/server.crt
        ln -sfv $APP_FOLDER/ssl/server.key /etc/ssl/server.key

        siteman -l
        service nginx configtest
        log "Restaring the server with new config..."
        sleep 2
        service nginx start

        #curl -sk https://localhost | grep -i 'olass'
    popd
}

function log() {
    echo -n "Log: "
    echo $*
}
