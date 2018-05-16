import io
import os
import unittest
import json
import random
import zipfile

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

def create_sample_data():
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

    def testDataGeneration(self):
        create_sample_data();
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

    def testPostData(self):
        data = self.generateSamplePostData()
        response, status = self.post_json_request('/datastore/', json.dumps(data), DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to post valid data while logged in.')

    def testGetData(self):
        data = self.generateSamplePostData()
        response, status = self.post_json_request('/datastore/', json.dumps(data), DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to post valid data while logged in.')

        storage_id = response['id']
        storage_rev = response['revision']
        
        response, status = self.get_json_response('/datastore/?store_id='+str(storage_id), DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to get valid data while logged in.')

        self.assertTrue( (
                storage_id == response['id']
                and storage_rev == response['revision']
                and isinstance(response['data'], list)
                and response['data'][0]['annotation'] == data['value'][0]['annotation']
            ), 'Expected matching data on a get response, using the id returned of a previous post request');

    def testGetList(self):
        DATA_AMOUNT = 12
        for i in range(DATA_AMOUNT):
            self.postRandomData()

        response, status = self.get_json_response('/datastore/list/', DEFAULT_HEADERS)
        self.assertEqual(len(response['list']), DATA_AMOUNT, 'Expected to get a list matching the amount of items that were just posted.')

    def testGetListByKey(self):
        DATA_AMOUNT = 6
        for i in range(int(DATA_AMOUNT / 2)):
            self.postRandomData()

        response_query, dataset_1 = self.postRandomData(True)
        response_1, status = response_query;
        self.assertEqual(200, status, 'Expected OK status when attempting to post valid data while logged in.')

        for i in range(int(DATA_AMOUNT / 2)):
            self.postRandomData()

        response_query, dataset_2 = self.postRandomData(True)
        response_2, status = response_query;
        self.assertEqual(200, status, 'Expected OK status when attempting to post valid data while logged in.')

        response, status = self.get_json_response('/datastore/list/'+dataset_1['key'], DEFAULT_HEADERS)
        self.assertEqual(response['list'][0]['id'], response_1['id'], 'Expected response to contain the storage object that was just posted.')

        response, status = self.get_json_response('/datastore/list/'+dataset_2['key'], DEFAULT_HEADERS)
        self.assertEqual(response['list'][0]['id'], response_2['id'], 'Expected response to contain the storage object that was just posted.')

        response, status = self.get_json_response('/datastore/?store_id='+str(response_1['id']), DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to get valid data while logged in.')
        self.assertEqual(response['key'], dataset_1['key'], 'Expected the newly added keys to match.')

        response, status = self.get_json_response('/datastore/?store_id='+str(response_2['id']), DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to get valid data while logged in.')
        self.assertEqual(response['key'], dataset_2['key'], 'Expected the newly added keys to match.')

    def testGetListByRevision(self):
        DATA_AMOUNT = 6
        REVISION_NAME = "test_revision"
        REVISION_NAME_2 = REVISION_NAME+"_backup"
        KEY = str(uuid.uuid4())

        for i in range(int(DATA_AMOUNT / 2)):
            self.postRandomData()

        dataset_1 = self.generateSamplePostData(key=KEY, revision=REVISION_NAME)
        response_1, status = self.post_json_request('/datastore/', json.dumps(dataset_1), DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to post valid data while logged in.')

        for i in range(int(DATA_AMOUNT / 2)):
            self.postRandomData()

        dataset_2 = self.generateSamplePostData(key=KEY, revision=REVISION_NAME_2)
        response, status = self.post_json_request('/datastore/', json.dumps(dataset_2), DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to post valid data while logged in.')

        response_1, status = self.get_json_response('/datastore/list/%s/%s'%(KEY, REVISION_NAME), DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to get valid data while logged in.')

        response_2, status = self.get_json_response('/datastore/list/%s/%s'%(KEY, REVISION_NAME_2), DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to get valid data while logged in.')

        self.assertTrue( (
                response_1['key'] == response_2['key']
                and response_1['revision'] == REVISION_NAME
                and response_2['revision'] == REVISION_NAME_2
                and response_1['list'][0]['id'] != response_2['list'][0]['id']
            ), 'Expected two separate storage objects that have the same key but differing revisions and values.')

    def testGetListByRevision(self):
        DATA_AMOUNT = 12
        for i in range(DATA_AMOUNT):
            self.postRandomData()

        data, is_json, status = self.get_file_response('/datastore/export/', DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to export valid data while logged in.')
        self.assertFalse(is_json, 'Expected streamed file data, not actual JSON response.')

        zip_archive = zipfile.ZipFile(io.BytesIO(data), "a", zipfile.ZIP_DEFLATED, False)
        archive_names = zip_archive.namelist()
        self.assertTrue(len(archive_names) == DATA_AMOUNT, 'Expected same amount of exported as amount posted.')

    """
    def testSegmentationNoAuth(self):
        response, status = self.get_json_response('/segment')
        self.assertEqual(401, status, 'Expected unauthorised status when attempting to segment without logging in.')

    def testSegmentationAuthNoDoc(self):
        response, status = self.get_json_response('/segment?remote_url='+ALVEO_API_URL, DEFAULT_HEADERS)
        self.assertTrue('Alveo document identifier' in response['description'], 'Expected error to be about the missing Alveo document identifier when authorised, attempting to segment without a document identifier.')
        self.assertEqual(400, status, 'Expected bad request status when attempting to segment without a document (via header).')

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
    """
