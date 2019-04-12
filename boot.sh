#!/bin/sh
# source venv/bin/activate
flask db upgrade
exec gunicorn -b :6000 --access-logfile - --error-logfile - solid_potato:app