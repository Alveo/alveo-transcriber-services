from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('../config')
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

@app.after_request
def after_request(response):
    """ This section is to allow the Alveo Transcriber to access this web application when hosted on a different address/domain. You can configure which origins are allowed in the global config file. """
    response.headers.add('Access-Control-Allow-Origin', app.config['ACCESS_CONTROL_ALLOW_ORIGIN'])
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

import application.views
