import json

from .alveo import AlveoTests

class AlveoDatastoreTests(AlveoTests):
    def testPostData(self):
        data = self.generateSamplePostData()
        response, status = self.post_json_request('/datastore/', json.dumps(data), self.DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to post valid data while logged in.')

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
