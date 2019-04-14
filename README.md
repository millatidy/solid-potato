# solid-potato
BriteCore Feature Request App

### How to download and run

git clone https://github.com/millatidy/solid-potato.git

cd solid-potato

pip install requirements.txt

export FLASK_APP=solid_potato.py
export FLASK_RUN_PORT=5001

if you want to run in debugging mode

export FLASK_DEBUG=1

### Migrate database
flask db init

flask db migrate

flask db upgrade

flask run
