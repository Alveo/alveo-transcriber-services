import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

config_file = os.environ.get("ATS_CONFIG_PATH", None)
if config_file is None:
    config_file == '../config'

app = Flask(__name__)
app.config.from_pyfile(config_file)
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
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

import application.views
