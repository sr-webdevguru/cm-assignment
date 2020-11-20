#!/usr/bin/env bash

# name of the virtual environment for staging
workon staging

# Project directory for dev
cd /git/api.staging.medic52.com/idalo_medic52dashboard/project/

# Django setup
pip install -r requirements/staging.txt
# (change) commented following three lines

#python manage.py makemigrations custom_user --settings=medic52.settings.staging
#python manage.py migrate custom_user --settings=medic52.settings.staging
#python manage.py makemigrations --settings=medic52.settings.staging
python manage.py migrate --settings=medic52.settings.staging

# New command 4/5/2015
python manage.py loaddata initial_data_staging --settings=medic52.settings.staging

python manage.py collectstatic --settings=medic52.settings.staging

# uWsgi reload
supervisorctl -c supervisord_staging.conf restart uwsgi

# Exists the virtual environment
deactivate