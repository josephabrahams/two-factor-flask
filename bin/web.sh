# !/bin/bash

if [[ (-n "$DEVEL") && ("`echo $DEVEL | tr '[A-Z]' '[a-z]'`" = "true") ]]; then
    # if $DEVEL is True then run the development server
    PYTHONUNBUFFERED=True python app.py runserver

else
    if [[ (-n "$DEBUG") && ("`echo $DEBUG | tr '[A-Z]' '[a-z]1'`" = "true") ]]; then
        # else run gunicorn with meinheld
        gunicorn --worker-class='egg:meinheld#gunicorn_worker' app:app --access-logfile - --error-logfile -
    else
        # don't keep access logs unless $DEBUG is True
        gunicorn --worker-class='egg:meinheld#gunicorn_worker' app:app --error-logfile -
    fi
fi
