# solid-potato
## BriteCore Feature Request App

### How to download and run
git clone https://github.com/millatidy/solid-potato.git<br>
cd solid-potato<br>
pip install requirements.txt<br>
export FLASK_APP=solid_potato.py<br>
if you want to run in debugging mode<br>
export FLASK_DEBUG=1<br>

### Migrate database
flask db init<br>
flask db migrate<br>
flask db upgrade<br>
flask run

# Deployment
Web Framework: Flask<br>
WSGI: Gunicorn<br>
Server: Nginx<br>
Container: Docker<br>
Ocherstration: Docker Compose<br>
OS: Ubuntu 18.04 LTS<br>
Platform: AWS EC2 t2.mirco<br>
Link: http://britecore.workshift.co.zw
