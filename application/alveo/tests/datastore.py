import json

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
                and isinstance(response['data'], list)
                and response['data'][0]['annotation'] == data['value'][0]['annotation']
            ), 'Expected matching data on a get response, using the id returned of a previous post request');
