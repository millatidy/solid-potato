# solid-potato
BriteCore Feature Request App

## How to download and run

git clone https://github.com/millatidy/solid-potato.git

cd solid-potato

pip install requirements.txt

export FLASK_APP=app.py

if you want to run in debugging mode
export FLASK_DEBUG=1

## Migrate database
flask db init
flask db migrate
flask db upgrade

flask run