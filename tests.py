import os
import unittest
import json

from application import app, db

API_KEY = None

class TestCase(unittest.TestCase):
    def get_json_response(self, path, headers={}):
        response = self.app.get(path, headers=headers)
        data = response.data.decode('utf8').replace("'", '"')
        return json.loads(data)

    #response = self.get_json_response('/authorize?api_key', {'Api-Key': API_KEY})
    def authenticate(self, aas_api_key):
        response = self.get_json_response('/authorize?api_key='+aas_api_key)

        if response['code'] is not 200:
            raise Exception("Could not authenticate with Alveo server. Response data: "+response)

        return response['ats-api-key']


    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.longMessage = True

        with app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def tearDown(self):
        pass

    def testCreation(self):
        response = self.get_json_response('/')
        self.assertEqual(404, response['status'])
        self.assertTrue('Resource not found' in response['description'])

    def testSegmentationNoAuth(self):
        response = self.get_json_response('/segment')
        self.assertEqual(401, response['status'], "Expected unauthorised status when attempting to segment without logging in.")

    def testAuthNoAPIKey(self):
        response = self.get_json_response('/authorize')
        self.assertEqual(400, response['status'], "Expected bad request status when attempting to authorize with no API key.")

    def testAuthInvalidAPIKey(self):
        # Test invalid API key via argument
        response = self.get_json_response('/authorize?api_key=0000000000')
        self.assertTrue('API key may be invalid' in response['description'], "Expected invalid API key response when attempting to authorize with an invalid Alveo API key.")
        self.assertEqual(400, response['status'], "Expected bad request status when attemping to authorize with an invalid API key.")

    def testValidAPIKey(self):
        # Test valid API key via argument
        response = self.get_json_response('/authorize?api_key='+API_KEY)
        self.assertEqual(200, response['status'], "Expected 200 response when sending a valid Alveo API key argument for authentication.")
        self.assertTrue(response['new_user'], "Expected to be flagged as a new user when registering for the first time. Is the test database being reused when it shouldn't be?")

if __name__ == '__main__':
    try:
        API_KEY = os.environ['ALVEO_API_KEY']
    except:
        print("Error: Alveo API key OS environment variable is not set. Cannot proceed.")

    if API_KEY is not None:
        unittest.main()
