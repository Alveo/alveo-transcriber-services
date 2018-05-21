import json

from application import db
from application.users.model import User
from application.datastore.model import Datastore

from application.alveo.module import DOMAIN
from .alveo import AlveoTests

class AlveoDatastoreTests(AlveoTests):
    def testPostData(self):
        data = self.generateSamplePostData()
        response, status = self.post_json_request('/datastore/', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to post valid data while logged in.')

    def testInvalidPostData(self):
        data = self.generateSamplePostData()
        data['value'][3]['thisshouldntwork'] = ''
        response, status = self.post_json_request('/datastore/', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(400, status, 'Expected invalid argument status when attempting to post invalid data while logged in.')
        self.assertTrue(response['description'].startswith("Invalid/unsupported key"), 'Expected message to be about an invalid/unsupported key.')

    def testMissingPostData(self):
        data = self.generateSamplePostData()
        data['value'][2].pop('start', None)
        response, status = self.post_json_request('/datastore/', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(400, status, 'Expected invalid argument status when attempting to post invalid data while logged in.')
        self.assertTrue(response['description'].startswith("Required key is missing"), 'Expected message to be about missing keys.')

    def testBadReplacedPostData(self):
        data = self.generateSamplePostData()
        data['value'][2].pop('start', None)
        data['value'][2]['starte'] = 0.3
        response, status = self.post_json_request('/datastore/', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(400, status, 'Expected invalid argument status when attempting to post invalid data while logged in.')
        self.assertTrue(response['description'].startswith("Invalid/unsupported key"), 'Expected message to be about an invalid/unsupported key.')

    def testBadTypePostData(self):
        data = self.generateSamplePostData()
        data['value'][3].pop('speaker', None)
        data['value'][3]['speaker'] = 1
        response, status = self.post_json_request('/datastore/', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(400, status, 'Expected invalid argument status when attempting to post invalid data while logged in.')
        self.assertTrue(response['description'].startswith("Invalid type for key"), 'Expected message to be about an invalid type for a key.')

        data = self.generateSamplePostData()
        data['value'][3].pop('start', None)
        data['value'][3]['start'] = "test"
        response, status = self.post_json_request('/datastore/', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(400, status, 'Expected invalid argument status when attempting to post invalid data while logged in.')
        self.assertTrue(response['description'].startswith("Invalid type for key"), 'Expected message to be about an invalid type for a key.')

    def testGetData(self):
        data = self.generateSamplePostData()
        response, status = self.post_json_request('/datastore/', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to post valid data while logged in.')

        storage_id = response['id']
        storage_rev = response['revision']
        
        response, status = self.get_json_response('/datastore/?store_id='+str(storage_id), self.DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to get valid data while logged in.')

        self.assertTrue( (
                storage_id == response['id']
                and storage_rev == response['revision']
                and isinstance(response['transcription'], list)
                and response['transcription'][0]['annotation'] == data['value'][0]['annotation']
            ), 'Expected matching data on a get response, using the id returned of a previous post request');

    def testOtherModuleFail(self):
        self.generateSampleAlveoData()

        user = User.query.filter(User.domain == DOMAIN).first()
        self.assertTrue(user != None, "Expected sample users to exist from generated sample data.")

        # Change the user's domain
        user.domain = "notalveo"
        db.session.commit()

        transcription = Datastore.query.filter(Datastore.user_id == user.id).first()
        self.assertTrue(transcription != None, "Expected sample transcription to exist from generated sample data.")

        response, status = self.get_json_response('/datastore/?store_id=%s'%transcription.id, self.DEFAULT_HEADERS)
        self.assertEqual(403, status, 'Expected forbidden status when attempting to get valid data from a different user on another domain, while logged in.')

