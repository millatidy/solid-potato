# Solid Potato
## Britecore's Feature Request WebApp
Solid Potato is a  web application that allows the user to create "feature requests". It was developed  as part of Britecore's Software Engineer (Implementation) job application process. The backend is provided via RESTAPI endpoints which feed and consume data to and from the frontend.

The live site for this application can be found on http://britecore.workshift.co.zw

# Application Requirements
Build a web application that allows the user to create "feature requests". The necessary fields are:

 1. Title: A short, descriptive name of the feature request.
 2. Description: A long description of the feature request.
 3. Client: A selection list of clients (use "Client A", "Client B", "Client C")
 4. Client Priority: A numbered priority according to the client (1...n). Client Priority numbers should not repeat for the given client, so if a priority is set on a new feature as "1", then all other feature requests for that client should be reordered.
 5. Target Date: The date that the client is hoping to have the feature.
 6. Product Area: A selection list of product areas (use 'Policies', 'Billing', 'Claims', 'Reports')

# Methodology
1. The application welcome page list's all (paginated, in multiples of 10) the feature requests stored in the database.
2. To enter a new feature request, user clicks on the New Feature button and a dialog appears where they enter the detials of the new feature.
   a. Title, Client, Priority and Product Area fields are required
   b. Title and Description fields are text fields
   c. Client and Product areas are drop down text fields
   d. Client priority is a number field with minimum possible number as 1
   e. Target Date field is an HTML5 date select field
   f. The miminum Target Date that can be set is 15 days from the current calender date
   d. If user does not enter/select Target Date, the system will by default set the Target Data to the 15th day from the current date
3. To edit a feature request, the user clicks on the edit button agaist a feature request. A Dialoge box will pop up with the feature details
   >NB: There is an [ISSUE] with this step
4. To delete a feature request, the user clicks the delete button against the feature request they want to delete. The application will refresh to list the requests on the current page
5. Client Priority numbers do not repeat. Say we have features F1, F2 and F3 for Client A with priority numbers 1, 2, 4 respectively. If we add feature F4 for client A with priority number 1, features F1, F2, priority numbers will be reordered to 2, and 3 respectively. This means for Client A, features F1, F2, F3 and F4 will have priority numbers 2, 3, 4 and 1 respectively
   > NB: To see the changes in client priority numbers after adding or editing a feature request, please refesh your page
5. A list of clients can be viewed on clicking the Clients navigation item. Each clients feature request can be viewed by clicking the view button under options
6. Clients and Product area details are considered to be out of scope of this application therefore despite having RESTAPI endpoints, no web interface is provided for their Creation, Updating and Deletion
7. An extra feature is the search function. The user can search features in the system. The system indexes each feature using its Title and Description
   >NB: The search feature is disabled on the [production site] because it is hosted on an AWS T2 Mircro Instance where ElasticSearch fails on startup due to memory issues.

# Tech

Solid Potato uses a number of open source projects to work properly:
## Frontend
* [JINJA] - is a full featured template engine for Python. To ease the pain of developing completely separate Frontend and Backend Application Jinja2 was used to as the html templating engine there flask framework(backend) easily manages the HTML templates, CSS and JavaScript files
* [Bootstrap] - a CSS framework directed at responsive, mobile-first front-end web development. I this project it is used to handle the application look and feel
* [Knockout JS] -  a JavaScript MVVM library that makes it easier to create rich, desktop-like user interfaces with JavaScript and HTML. It is used to render and refresh data on the web browser interface
* [jQuery] - a JavaScript Library used in this instance to make AJAX requests to the API simpler

## Backend
* [Flask] - a Python based microframework used in this instance to build a REST API backend
* [ElasticSearch] - a Java Search Engine that provides a distributed,  multitenant-capable fulltext search. Its use is to provide the application with the capability of full text search
* [Flask-SQLAlchemy] - n extension for Flask that adds support for [SQLAlchemy] to your application. It is an Object-Relatational Mapping tool the abstract database specific code for our appplication
* [Flask-Migrate] - an extension that handles [SQLAlchemy] database migrations for Flask applications using [Alembic]. As we upgrade or make changes to our application schema, [Flask-Migrate] eases the pain of upgrading the database schema of an aleardy existing database. It alse keeps track of database version changes therefore downgrades are made easier too
* [Sentry] - an error tracking service that helps us monitor and fix crashes in realtime. [Sentry] Logs any errors that occur in our application
* [PostgreSQL] - an open-source relational database management system. The application data is stored in this database

## Deployment
* [Docker] - a software platform designed to make it easier to create, deploy, and run applications by using containers. Both our backend and frontend as well as WSGI HTTP Server are bundled into a single application and containerized into a docker container
* [Docker Compose] - a tool for defining and running multi-container Docker applications. In this instance docker compose was used to glue together our front facing Server and our WSGI Server, set our backend Environment Variables, and provide the a link to our web application start commands
* [Gunicorn] - a Python WSGI HTTP Server for UNIX. It is placed in front of flask for production environment
* [Nginx] - an open source HTTP Web server in this instance used as a reverse proxy server to the Gunicorn server. It is our front facing Server. It is also responsible for enforcing a Content Security Policy, and prevent attacks like Cross Site Scripting and Clickjacking

## Operating System
* [Ubuntu] - an open-source Linux distribution based on Debian. Our system runs in an Ubuntu server

## Servers
* [AWS RDS] -  a web service that makes it easier to set up, operate, and scale a relational database in the cloud. Our PostgreSQL database is hosted on [AWS RDS]
* [AWS EC2]- a web service that provides secure, resizable compute capacity in the cloud. It is designed to make web-scale cloud computing easier for developers. Our dockerized application's i.e. Nginx Server and Web Application Server containers are hosted on a AWS t2.micro instance running [Ubuntu]

# Installation
```sh
$ git clone https://github.com/millatidy/solid-potato.git
$ cd solid-potato
$ pip install requirements.txt
$ export FLASK_APP=solid_potato.py
```

## Database setup
```sh
$ flask db init
$ flask db migrate
$ flask db upgrade
```

## Environment Variables
```sh
$ DATABASE_URL=`your.database.endpoint`
$ ELASTICSEARCH_URL=`your.elasticsearch.endpoint`
```
>NB: In dev you can leave out both the enviroment vairables. The application will use the default sqlite url and disable [ElasticSearch]

## Run Application
```sh
$ flask run
```
The application web interface will run on http://localhost:5000 and the api on http://localhost:5000/api

if you want to run the applicatoin in debugging mode, make the following export before run
```sh
$ export FLASK_DEBUG=1
```
>WARINING: *FOR DEVELOPEMENT ENVIRONMENT ONLY*

## For production environments...
In the docker-compose.yml file under environment please set up.

```sh
$ DATABASE_URL=`your.database.endpoint`
```
>*Do not let the application run using default Sqlite database in production*
if you have an active [ElasticSearch] backend otherwise the application will disable the search feature
```sh
$ ELASTICSEARCH_URL=`your.elasticsearch.endpoint`
```
>NB: Make sure FLASK_DEBUG is set to 0 when in production

# Development

This repository is not open for contributions but what you do with the source is up to you.


   [git-repo-url]: <https://github.com/millatidy/solid-potato.git>
   [production site]: <http://britecore.workshift.co.zw>
   [JINJA]: <http://jinja.pocoo.org/>
   [Bootstrap]: <https://getbootstrap.com/>
   [Knockout JS]: <https://knockoutjs.com/>
   [jQuery]: <http://jquery.com>
   [Flask]: <http://flask.pocoo.org/>
   [Flask-SQLAlchemy]: <https://flask-sqlalchemy.palletsprojects.com/>
   [SQLALchemy]: <https://www.sqlalchemy.org/>
   [Flask-Migrate]: <https://flask-migrate.readthedocs.io/en/latest/>
   [Alembic]: <https://alembic.sqlalchemy.org/en/latest/>
   [Sentry]: <https://github.com/getsentry/sentry>
   [PostgreSQL]: <https://www.postgresql.org/>
   [ElasticSearch]: <https://www.elastic.co/>
   [Docker]: <https://www.docker.com/>
   [Docker Compose]: <https://www.docker.com/compose/>
   [Gunicorn]: <https://gunicorn.org/>
   [Nginx]: <https://www.nginx.com/>
   [AWS EC2]: <https://aws.amazon.com/ec2/>
   [AWS RDS]: <https://aws.amazon.com/rds/>
   [Ubuntu]: <https://www.ubuntu.com/>
   [ISSUE]: <https://github.com/millatidy/solid-potato/issues/8>
