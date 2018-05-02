import os
import unittest
import json

from application import app, db

ALVEO_API_KEY = None
DEFAULT_HEADERS = None

class TestCase(unittest.TestCase):
    def get_json_response(self, path, headers={}):
        response = self.app.get(path, headers=headers)
        data = response.data.decode('utf8').replace('\'', '"')
        return json.loads(data), response.status_code

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

    def testSegmentationNoAuth(self):
        response, status = self.get_json_response('/segment')
        self.assertEqual(401, status, 'Expected unauthorised status when attempting to segment without logging in.')

    def testSegmentationAuthNoDoc(self):
        response, status = self.get_json_response('/segment?remote_url='+app.config['ALVEO_API_URL'], DEFAULT_HEADERS)
        self.assertTrue('Alveo document identifier' in response['description'], 'Expected error to be about the missing Alveo document identifier when authorised, attempting to segment without a document identifier.')
        self.assertEqual(400, status, 'Expected bad request status when attempting to segment without a document (via header).')

    def testSegmentationAuthExpiredAlveoKey(self):
        pass # TODO not implemented: no way to unauthorise at this time, without restarting server using persistent database

    def testSegmentationInvalidDocument(self):
        invalid_remote_url = 'https://app.alveo.edu.au/catalog/doesnot/exist.wav'
        response, status = self.get_json_response('/segment?remote_url='+invalid_remote_url, DEFAULT_HEADERS)
        self.assertTrue('Could not access requested doc' in response['description'], 'Expected error to be about an inaccessible Alveo document identifier when attempting to segment with an invalid document identifier.')
        self.assertEqual(400, status, 'Expected bad request status when attempting to segment an invalid document.')

    def testSegmentationValidDocument(self):
        remote_url = 'https://app.alveo.edu.au/catalog/austalk/1_1274_2_7_001/document/1_1274_2_7_001-ch6-speaker16.wav'

        response, status = self.get_json_response('/segment?remote_url='+remote_url, DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected status OK when attempting to segment a valid document.')
        self.assertTrue(len(response['results']) > 0, 'Expected a list of segments when segmenting a valid document.')
        results = response['results']

        response, status = self.get_json_response('/segment?remote_url='+remote_url, DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected status OK when attempting to segment a valid document, again (cache check).')
        self.assertTrue(len(response['results']) > 0, 'Expected a list of segments when segmenting a valid document, again (cache check).')
        cached_results = response['results']

        self.assertTrue(len(results) is len(cached_results), 'Expected the original segmentation results to match the number of cached segmentation results when segmenting twice.')


if __name__ == '__main__':
    try:
        ALVEO_API_KEY = os.environ['ALVEO_API_KEY']
        DEFAULT_HEADERS = {
                    'X-Api-Key': ALVEO_API_KEY,
                    'X-Api-Domain': 'app.alveo.edu.au'
                }
    except:
        print('Error: ALVEO_API_KEY environment variable is not set. Cannot proceed.')

    if ALVEO_API_KEY is not None:
        unittest.main()
