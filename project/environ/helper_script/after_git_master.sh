#!/usr/bin/env bash

# name of the virtual environment for master
workon master

# Project directory for master
cd /git/api.medic52.com/idalo_medic52dashboard/project/

# Django setup
pip install -r requirements/master.txt
# (change) commented following three lines

#python manage.py makemigrations custom_user --settings=medic52.settings.master
#python manage.py migrate custom_user --settings=medic52.settings.master
#python manage.py makemigrations --settings=medic52.settings.master
python manage.py migrate --settings=medic52.settings.master

# New command 4/5/2015
python manage.py loaddata initial_data_master --settings=medic52.settings.master

python manage.py collectstatic --settings=medic52.settings.master

# uWsgi reload
supervisorctl -c supervisord_master.conf restart uwsgi

# Exists the virtual environment
deactivate