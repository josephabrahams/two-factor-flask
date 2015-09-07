#!/bin/sh

if [ $(echo "$DEVEL" | tr '[A-Z]' '[a-z]') = 'true' ]; then
    PYTHONUNBUFFERED=True python app.py runserver
else
    if [ $(echo "$DEBUG" | tr '[A-Z]' '[a-z]') = 'true' ]; then
        gunicorn --worker-class='egg:meinheld#gunicorn_worker' app:app --access-logfile - --error-logfile -
    else
        gunicorn --worker-class='egg:meinheld#gunicorn_worker' app:app --error-logfile -
    fi
fi
