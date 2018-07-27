import os
import unittest
import json

os.environ['ATS_ENVIRONMENT'] = 'application.config.TestEnvironment'
from application import app, db

from application.users.model import User 
from application.datastore.model import Datastore

try:
    from application.alveo.tests import *
except Exception as e:
    print("Skipping Alveo tests. Reason: ", e)

class ATSTests(unittest.TestCase):
    def setUp(self):
        # Override default URI
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.DEFAULT_HEADERS = None

        self.app = app.test_client()
        self.longMessage = True

        # Recreate session
        with app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()
        pass

    def tearDown(self):
        pass

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
                follow_redirects=False,
                content_type='application/json'
            )
        return response.json, response.status_code

    def createSampleData(self):
        domain = "mountains"
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
        self.createSampleData();
        users = User.query.all();
        self.assertEqual(8, len(users))

    def generateSamplePostData(self, key=None, fields=None, revision=None):
        raise NotImplementedError

    def postRandomData(self, return_sample=False, domain=''):
        data = self.generateSamplePostData()
        response = self.post_json_request(domain+'/datastore/objects', json.dumps(data), self.DEFAULT_HEADERS)
        if return_sample:
            return response, data
        return response

if __name__ == '__main__':
    unittest.main()
