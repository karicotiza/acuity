#!/bin/bash

python manage.py migrate && \
python manage.py collectstatic --noinput && \
python manage.py createsuperuser --noinput || true && \
uwsgi --ini core.uwsgi.ini