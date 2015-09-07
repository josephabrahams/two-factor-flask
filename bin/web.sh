#!/bin/sh

if [ $FLASK_ENV = "development" ]; then
    PYTHONUNBUFFERED=True python foo.py runserver
else
    if [ $DEBUG = "True" ]; then
        gunicorn --worker-class="egg:meinheld#gunicorn_worker" foo:app --access-logfile - --error-logfile -
    else
        gunicorn --worker-class="egg:meinheld#gunicorn_worker" foo:app --error-logfile -
    fi
fi
