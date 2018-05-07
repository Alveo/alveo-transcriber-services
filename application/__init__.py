import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
environment = os.environ.get('ATS_ENVIRONMENT', 'application.config.ProductionEnvironment')
app.config.from_object(environment)

if app.config['SQLALCHEMY_DATABASE_URI'] is None:
    if not app.debug:
        raise Exception("SQLALCHEMY_DATABASE_URI is not specified. Cannot continue.")
    else:
        path = '/tmp/alveots-test.db'
        print("WARNING: Because debug is enabled, using `%s` as no database has been specified as SQLALCHEMY_DATABASE_URI env variable has not been set." % path)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
events = {}
event_types = {
        'auth': None,
        'segmentation': None,
        'store': None,
        'retrieve': None
    }

@app.after_request
def after_request(response):
    """ This section is to allow the Alveo Transcriber to access this web application when hosted on a different address/domain. You can configure which origins are allowed in the global config file. """
    response.headers.add('Access-Control-Allow-Origin', app.config['ACCESS_CONTROL_ALLOW_ORIGIN'])
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Api-Domain')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

import application.views
