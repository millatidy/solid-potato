from flask import Flask , current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_cors import CORS
from elasticsearch import Elasticsearch
from raven.contrib.flask import Sentry

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
sentry = Sentry()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	migrate.init_app(app, db)
	cors.init_app(app, resources={r"/*": {
									"origins": [
										"http://0.0.0.0:5000"
										]
									}
								})

	from app.main import bp as main_bp
	app.register_blueprint(main_bp)

	# from app.errors import bp as msg_bp
	# app.register_blueprint(msg_bp)
	

	from app.api import bp as api_bp
	app.register_blueprint(api_bp, url_prefix="/api")


	app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
	if app.config['ELASTICSEARCH_URL'] else None


	if not app.debug:
		# Sentry
		sentry.init_app(app, dsn='https://f70b58dfecda4089b51567122c36a881:4fcb5bf1b52f4ddc974db998dc3f1fd2@sentry.io/1292364')

	return app

from app import models, messages