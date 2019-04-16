# solid-potato
BriteCore Feature Request App

### How to download and run

git clone https://github.com/millatidy/solid-potato.git

cd solid-potato

pip install requirements.txt

export FLASK_APP=solid_potato.py

if you want to run in debugging mode

export FLASK_DEBUG=1

### Migrate database
flask db init

flask db migrate

flask db upgrade

flask run

# Deployment
Web Framework: Flask
WSGI: Gunicorn
Server: Nginx
Container: Docker
Ocherstration: Docker Compose
Platform: AWS EC2 t2.mirco
Link: http://britecore.workshift.co.zw
