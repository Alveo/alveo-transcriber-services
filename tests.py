import os
import unittest
import json

from application import app, db

ALVEO_API_KEY = None

class TestCase(unittest.TestCase):
    def get_json_response(self, path, headers={}):
        response = self.app.get(path, headers=headers)
        data = response.data.decode('utf8').replace('\'', '"')
        return json.loads(data)

    #response = self.get_json_response('/authorize?api_key', {'Api-Key': ALVEO_API_KEY})
    def authenticate(self, aas_api_key):
        response = self.get_json_response('/authorize?api_key='+aas_api_key)

        if response['status'] is not 200:
            raise Exception('Could not authenticate with Alveo server. Response data: '+response)

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

    def testAuthNoAPIKey(self):
        response = self.get_json_response('/authorize')
        self.assertEqual(400, response['status'], 'Expected bad request status when attempting to authorize with no API key.')

    def testAuthInvalidAPIKey(self):
        response = self.get_json_response('/authorize?api_key=0000000000')
        self.assertTrue('API key may be invalid' in response['description'], 'Expected invalid API key response when attempting to authorize with an invalid Alveo API key.')
        self.assertEqual(400, response['status'], 'Expected bad request status when attemping to authorize with an invalid API key.')

    def testValidAPIKey(self):
        response = self.get_json_response('/authorize?api_key='+ALVEO_API_KEY)
        self.assertEqual(200, response['status'], 'Expected 200 response when sending a valid Alveo API key argument for authentication.')
        self.assertTrue(response['new_user'], 'Expected to be flagged as a new user when registering for the first time. Is the test database being reused when it shouldn\'t be?')

        response = self.get_json_response('/authorize?api_key='+ALVEO_API_KEY)
        self.assertEqual(200, response['status'], 'Expected 200 response when sending a valid Alveo API key argument for authentication, a second time.')
        self.assertFalse(response['new_user'], 'Expected to NOT be flagged as a new user when authenticating after the first time.')

    def testSegmentationNoAuth(self):
        response = self.get_json_response('/segment')
        self.assertEqual(401, response['status'], 'Expected unauthorised status when attempting to segment without logging in.')

    def testSegmentationAuthArgumentNoDoc(self):
        ATS_API_KEY = self.authenticate(ALVEO_API_KEY)

        response = self.get_json_response('/segment?api_key='+ATS_API_KEY)
        self.assertTrue('Alveo document identifier' in response['description'], 'Expected error to be about the missing Alveo document identifier when authorised, attempting to segment without a document identifier.')
        self.assertEqual(400, response['status'], 'Expected bad request status when attempting to segment without a document (via arugment).')

    def testSegmentationAuthHeaderNoDoc(self):
        ATS_API_KEY = self.authenticate(ALVEO_API_KEY)

        response = self.get_json_response('/segment', {'Api-Key': ATS_API_KEY})
        self.assertTrue('Alveo document identifier' in response['description'], 'Expected error to be about the missing Alveo document identifier when authorised, attempting to segment without a document identifier.')
        self.assertEqual(400, response['status'], 'Expected bad request status when attempting to segment without a document (via header).')

    def testSegmentationAuthExpiredAlveoKey(self):
        pass # TODO not implemented: no way to unauthorise at this time, without restarting server using persistent database

    def testSegmentationInvalidDocument(self):
        ATS_API_KEY = self.authenticate(ALVEO_API_KEY)

        invalid_document_id = 'https://app.alveo.edu.au/catalog/doesnot/exist.wav'
        response = self.get_json_response('/segment?document_id='+invalid_document_id, {'Api-Key': ATS_API_KEY})
        self.assertTrue('Could not access requested doc' in response['description'], 'Expected error to be about an inaccessible Alveo document identifier when attempting to segment with an invalid document identifier.')
        self.assertEqual(400, response['status'], 'Expected bad request status when attempting to segment an invalid document.')

    def testSegmentationValidDocument(self):
        ATS_API_KEY = self.authenticate(ALVEO_API_KEY)

        document_id = 'https://app.alveo.edu.au/catalog/austalk/1_1274_2_7_001/document/1_1274_2_7_001-ch6-speaker16.wav'

        response = self.get_json_response('/segment?document_id='+document_id, {'Api-Key': ATS_API_KEY})
        self.assertEqual(200, response['status'], 'Expected status OK when attempting to segment a valid document.')
        self.assertTrue(len(response['result']) > 0, 'Expected a list of segments when segmenting a valid document.')
        results = response['result']

        response = self.get_json_response('/segment?document_id='+document_id, {'Api-Key': ATS_API_KEY})
        self.assertEqual(200, response['status'], 'Expected status OK when attempting to segment a valid document, again (cache check).')
        self.assertTrue(len(response['result']) > 0, 'Expected a list of segments when segmenting a valid document, again (cache check).')
        cached_results = response['result']

        self.assertTrue(len(results) is len(cached_results), 'Expected the original segmentation results to match the number of cached segmentation results when segmenting twice.')


if __name__ == '__main__':
    try:
        ALVEO_API_KEY = os.environ['ALVEO_API_KEY']
    except:
        print('Error: ALVEO_API_KEY environment variable is not set. Cannot proceed.')

    if ALVEO_API_KEY is not None:
        unittest.main()
