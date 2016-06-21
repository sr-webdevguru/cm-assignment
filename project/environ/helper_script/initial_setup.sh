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

# Exists the virtual environment
deactivate

# name of the virtual environment for staging
workon staging

# Project directory for staging
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

# Exists the virtual environment
deactivate

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

# Exists the virtual environment
deactivate