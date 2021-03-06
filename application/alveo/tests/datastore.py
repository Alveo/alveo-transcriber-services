import json

from application import db
from application.users.model import User
from application.datastore.model import Datastore

from application.alveo.module import DOMAIN
from .alveo import AlveoTests


class AlveoDatastoreTests(AlveoTests):
    def testPostData(self):
        data = self.generateSamplePostData()
        response, status = self.post_json_request(
            DOMAIN + '/datastore/objects', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to post valid data while logged in.')

    def testInvalidPostData(self):
        data = self.generateSamplePostData()
        data['value'][3]['thisshouldntwork'] = ''
        response, status = self.post_json_request(
            DOMAIN + '/datastore/objects', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(
            400,
            status,
            'Expected invalid argument status when attempting to post invalid data while logged in.')
        self.assertTrue(
            response['description'].startswith("Invalid/unsupported key"),
            'Expected message to be about an invalid/unsupported key.')

    def testMissingPostData(self):
        data = self.generateSamplePostData()
        data['value'][2].pop('start', None)
        response, status = self.post_json_request(
            DOMAIN + '/datastore/objects', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(
            400,
            status,
            'Expected invalid argument status when attempting to post invalid data while logged in.')
        self.assertTrue(
            response['description'].startswith("Required key is missing"),
            'Expected message to be about missing keys.')

    def testBadReplacedPostData(self):
        data = self.generateSamplePostData()
        data['value'][2].pop('start', None)
        data['value'][2]['starte'] = 0.3
        response, status = self.post_json_request(
            DOMAIN + '/datastore/objects', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(
            400,
            status,
            'Expected invalid argument status when attempting to post invalid data while logged in.')
        self.assertTrue(
            response['description'].startswith("Invalid/unsupported key"),
            'Expected message to be about an invalid/unsupported key.')

    def testBadTypePostData(self):
        data = self.generateSamplePostData()
        data['value'][3].pop('speaker', None)
        data['value'][3]['speaker'] = 1
        response, status = self.post_json_request(
            DOMAIN + '/datastore/objects', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(
            400,
            status,
            'Expected invalid argument status when attempting to post invalid data while logged in.')
        self.assertTrue(
            response['description'].startswith("Invalid type for key"),
            'Expected message to be about an invalid type for a key.')

        data = self.generateSamplePostData()
        data['value'][3].pop('start', None)
        data['value'][3]['start'] = "test"
        response, status = self.post_json_request(
            DOMAIN + '/datastore/objects', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(
            400,
            status,
            'Expected invalid argument status when attempting to post invalid data while logged in.')
        self.assertTrue(
            response['description'].startswith("Invalid type for key"),
            'Expected message to be about an invalid type for a key.')

    def testGetData(self):
        data = self.generateSamplePostData()
        response, status = self.post_json_request(
            DOMAIN + '/datastore/objects', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to post valid data while logged in.')

        storage_id = response['id']

        response, status = self.get_json_response(
            DOMAIN + '/datastore/objects/%s' % storage_id, self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to get valid data while logged in.')

        self.assertTrue(
            (storage_id == response['id'] and isinstance(
                response['transcription'],
                list) and response['transcription'][0]['caption'] == data['value'][0]['caption']),
            'Expected matching data on a get response, using the id returned of a previous post request')

    def testGetVersionedData(self):
        data = self.generateSamplePostData()
        response, status = self.post_json_request(
            DOMAIN + '/datastore/objects', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to post valid data while logged in.')

        storage_id = response['id']

        response_1, status = self.get_json_response(
            DOMAIN + '/datastore/objects/%s/0' % storage_id, self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to get valid data while logged in.')

        data_2 = data
        data_2['value'][0]['caption'] = "REPLACED!"

        response, status = self.post_json_request(
            DOMAIN + '/datastore/objects', json.dumps(data_2), self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to post valid data while logged in.')


        response_2, status = self.get_json_response(
            DOMAIN + '/datastore/objects/%s/1' % storage_id, self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to get valid data while logged in.')

        self.assertTrue(
            response_1['transcription'] != response_2['transcription'] and response_2['transcription'][0]['caption'] == "REPLACED!",
            'Expected matching data on a get response, using the id returned of a previous post request')

        self.assertEqual(
            response_1['version'], 0,
            "Expected first response to be version 0.")

        self.assertEqual(
            response_2['version'], 1,
            "Expected second response to be version 1.")

        self.assertEqual(
            response_1['total_versions'], 1,
            "Expected first response to know of one version.")

        self.assertEqual(
            response_2['total_versions'], 2,
            "Expected second response to know of two versions.")

    def testOtherModuleFail(self):
        self.generateSampleAlveoData()

        user = User.query.filter(User.domain == DOMAIN).first()
        self.assertTrue(
            user is not None,
            "Expected sample users to exist from generated sample data.")

        # Change the user's domain
        user.domain = "notalveo"
        db.session.commit()

        transcription = Datastore.query.filter(
            Datastore.user_id == user.id).first()
        self.assertTrue(
            transcription is not None,
            "Expected sample transcription to exist from generated sample data.")

        response, status = self.get_json_response(
            DOMAIN + '/datastore/objects/%s' %
            transcription.id, self.DEFAULT_HEADERS)
        self.assertEqual(
            403,
            status,
            'Expected forbidden status when attempting to get valid data from a different user on another domain, while logged in.')
