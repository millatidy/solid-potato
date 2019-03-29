from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_cors import CORS
# from flask_mail import Mail
from raven.contrib.flask import Sentry

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app, resources={r"/*": {
									"origins": [
										"http://localhost:8080"
										]
									}
								}
							)
# mail = Mail(app)

if not app.debug:
	# Sentry
	sentry = Sentry(app, dsn='https://f70b58dfecda4089b51567122c36a881:4fcb5bf1b52f4ddc974db998dc3f1fd2@sentry.io/1292364')

from app import routes, models, messages