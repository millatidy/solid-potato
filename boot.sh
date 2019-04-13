#!/bin/sh
# source venv/bin/activate
flask db upgrade
exec gunicorn -b :5001 --access-logfile - --error-logfile - solid_potato:app
