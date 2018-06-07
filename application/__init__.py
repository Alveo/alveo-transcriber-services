import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
environment = os.environ.get(
    'ATS_ENVIRONMENT', 'application.config.ProductionEnvironment')
app.config.from_object(environment)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute"]
)

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

@app.after_request
def after_request(response):
    """ Processes a ready-to-send response

    This will tell the application what we expect back in terms of valid headers, and
    enable more complicated website applications to  access this web application when
    hosted on a different address/domain. You can configure which origins are allowed
    in the global config file.

    Args:
        Response: Flask response object
    
    """
    response.headers.add('Access-Control-Allow-Origin',
                         app.config['ACCESS_CONTROL_ALLOW_ORIGIN'])
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,X-Api-Domain,X-Api-Key')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
events = {}

import application.views
