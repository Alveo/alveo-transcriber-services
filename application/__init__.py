import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from redis import Redis
from rq import Queue

app = Flask(__name__)
environment = os.environ.get(
    'ATS_ENVIRONMENT', 'application.config.ProductionEnvironment')
app.config.from_object(environment)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute"]
)
redis_queue = Queue(connection=Redis())
CORS(app)

if app.config['SQLALCHEMY_DATABASE_URI'] is None:
    if not app.config['TESTING']:
        if not app.debug:
            raise Exception(
                "DATABASE_URL environment variable has not specified. Cannot continue.")
        if app.debug:
            path = '/tmp/alveots-test.db'
            print(
                "WARNING: Because debug is enabled, using `%s` as no database has been specified as DATABASE_URL environment variable has not been set." %
                path)
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
events = {}

import application.views