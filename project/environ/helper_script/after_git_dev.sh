#!/usr/bin/env bash

# name of the virtual environment for dev
workon dev

# Project directory for dev
cd /git/api.dev.medic52.com/idalo_medic52dashboard/project/

# Django setup
pip install -r requirements/dev.txt
# (change) commented following three lines

#python manage.py makemigrations custom_user --settings=medic52.settings.dev
#python manage.py migrate custom_user --settings=medic52.settings.dev
#python manage.py makemigrations --settings=medic52.settings.dev
python manage.py migrate --settings=medic52.settings.dev

# New command 4/5/2015
python manage.py loaddata initial_data_dev --settings=medic52.settings.dev

python manage.py collectstatic --settings=medic52.settings.dev

# uWsgi reload
supervisorctl -c supervisord_dev.conf restart uwsgi

# Exists the virtual environment
deactivate