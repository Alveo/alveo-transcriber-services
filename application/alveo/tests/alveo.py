import os
import unittest
import json
import random

import uuid

from application import app, db
from application.misc.events import get_module_metadata

from application.users.model import User 
from application.datastore.model import Datastore

ALVEO_API_KEY = None
ALVEO_API_URL = os.environ.get
DEFAULT_HEADERS = None

alveo_metadata = get_module_metadata('alveo')

if alveo_metadata is None:
    raise Exception('Module not loaded in app configuration.')

ALVEO_API_URL = alveo_metadata['api_url']
ALVEO_API_KEY = os.environ.get('ALVEO_API_KEY', None)

if ALVEO_API_KEY is None:
    raise Exception('ALVEO_API_KEY environment variable is not set. Cannot proceed.')

DEFAULT_HEADERS = {
            'X-Api-Key': ALVEO_API_KEY,
            'X-Api-Domain': 'app.alveo.edu.au'
        }

class AlveoTests(unittest.TestCase):
    def get_json_response(self, path, headers=None):
        response = self.app.get(path, headers=headers)
        return response.json, response.status_code

    def get_file_response(self, path, headers=None):
        response = self.app.get(path, headers=headers)
        return response.get_data(), response.is_json, response.status_code

    def post_json_request(self, path, data, headers=None):
        response = self.app.post(
                path,
                data=data,
                headers=headers,
                follow_redirects=False, # Do not set to true as Flask will not resend headers
                content_type='application/json'
            )
        return response.json, response.status_code

    def setUp(self):
        self.ALVEO_API_URL = ALVEO_API_URL
        self.DEFAULT_HEADERS = DEFAULT_HEADERS

        # Override default URI
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.app = app.test_client()
        self.longMessage = True

        # Recreate session
        with app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def tearDown(self):
        pass

    def create_sample_data(self):
        domain = "alveo"
        alveo_10 = User("10", domain)
        alveo_150 = User("150", domain)
        alveo_475 = User("475", domain)
        db.session.add(alveo_10)
        db.session.add(alveo_150)
        db.session.add(alveo_475)

        domain = "generic"
        generic_10 = User("10", domain)
        generic_91042 = User("91042", domain)
        db.session.add(generic_10)
        db.session.add(generic_91042)

        domain = "testdomain"
        testdomain_12084013 = User("12084013", domain)
        testdomain_0 = User("0", domain)
        testdomain_50 = User("50", domain)
        db.session.add(testdomain_12084013)
        db.session.add(testdomain_0)
        db.session.add(testdomain_50)

    def testDataGeneration(self):
        self.create_sample_data();
        users = User.query.all();
        self.assertEqual(8, len(users))

    def generateSamplePostData(self, key=None, fields=None, revision=None):
        if key is None:
            key = str(uuid.uuid4())
        if fields is None:
            fields = random.randint(5, 15)

        data = {
            "key": key,
            "value": []
        }

        if revision is not None:
            data['revision'] = revision

        start = 0
        end = 0
        for i in range(fields):
            start = end + random.uniform(0.3, 5)
            end = start + random.uniform(3, 7)
            annotation = {
                "start": start,
                "end": end,
                "speaker": str(random.randint(1, 1000)),
                "annotation": str(uuid.uuid4())
              }
            data["value"].append(annotation)

        return data

    def postRandomData(self, return_sample=False):
        data = self.generateSamplePostData()
        if return_sample:
            return self.post_json_request('/datastore/', json.dumps(data), DEFAULT_HEADERS), data
        return self.post_json_request('/datastore/', json.dumps(data), DEFAULT_HEADERS)
