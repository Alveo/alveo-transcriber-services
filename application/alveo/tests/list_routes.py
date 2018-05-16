import uuid
import json

from application import db
from application.users.model import User
from application.datastore.model import Datastore

from application.alveo.module import DOMAIN
from .alveo import AlveoTests

class AlveoListRoutesTests(AlveoTests):
    def testGetList(self):
        DATA_AMOUNT = 12
        for i in range(DATA_AMOUNT):
            self.postRandomData()

        response, status = self.get_json_response('/datastore/list/', self.DEFAULT_HEADERS)
        self.assertEqual(len(response['storage_objects']), DATA_AMOUNT, 'Expected to get a list matching the amount of items that were just posted.')

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

        response, status = self.get_json_response('/datastore/list/'+dataset_1['key'], self.DEFAULT_HEADERS)
        self.assertEqual(response['storage_objects'][0]['id'], response_1['id'], 'Expected response to contain the storage object that was just posted.')

        response, status = self.get_json_response('/datastore/list/'+dataset_2['key'], self.DEFAULT_HEADERS)
        self.assertEqual(response['storage_objects'][0]['id'], response_2['id'], 'Expected response to contain the storage object that was just posted.')

        response, status = self.get_json_response('/datastore/?store_id='+str(response_1['id']), self.DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to get valid data while logged in.')
        self.assertEqual(response['key'], dataset_1['key'], 'Expected the newly added keys to match.')

        response, status = self.get_json_response('/datastore/?store_id='+str(response_2['id']), self.DEFAULT_HEADERS)
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
        response_1, status = self.post_json_request('/datastore/', json.dumps(dataset_1), self.DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to post valid data while logged in.')

        for i in range(int(DATA_AMOUNT / 2)):
            self.postRandomData()

        dataset_2 = self.generateSamplePostData(key=KEY, revision=REVISION_NAME_2)
        response, status = self.post_json_request('/datastore/', json.dumps(dataset_2), self.DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to post valid data while logged in.')

        response_1, status = self.get_json_response('/datastore/list/%s/%s'%(KEY, REVISION_NAME), self.DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to get valid data while logged in.')

        response_2, status = self.get_json_response('/datastore/list/%s/%s'%(KEY, REVISION_NAME_2), self.DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to get valid data while logged in.')

        self.assertTrue( (
                response_1['query_key'] == response_2['query_key']
                and response_1['query_revision'] == REVISION_NAME
                and response_2['query_revision'] == REVISION_NAME_2
                and response_1['storage_objects'][0]['id'] != response_2['storage_objects'][0]['id']
            ), 'Expected two separate storage objects that have the same key but differing revisions and values.')

    def testOtherModuleFail(self):
        pass

    def testOtherUserList(self):
        self.generateSampleAlveoData()
        users = User.query.filter(User.domain == DOMAIN).all()

        # Note: Our user doesn't exist yet since the database is rebuilt each
        #  time. We'll only be added after our first successful request. So we can use whoever
        #  we want from the sample pool without risk of getting our own test user.

        self.assertTrue(len(users) > 0, "Expected sample users to exist from generated sample data.")

        user_1 = users[0].id
        user_2 = users[1].id

        transcription_list_1 = Datastore.query.filter(Datastore.user_id == user_1).all()
        transcription_list_2 = Datastore.query.filter(Datastore.user_id == user_2).all()
        transcription_1 = transcription_list_1[0]
        transcription_2 = transcription_list_2[0]

        db.session.expunge_all()

        self.assertTrue(len(transcription_list_1) > 0, "Expected sample transcriptions to exist from generated sample data.")
        self.assertTrue(len(transcription_list_2) > 0, "Expected sample transcriptions to exist from generated sample data.")

        response, status = self.get_json_response('/datastore/user/%s/list/'%user_1, self.DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to get valid data while logged in.')
        self.assertEqual(len(response['storage_objects']), len(transcription_list_1), 'Expected the newly added keys to match.')

        response, status = self.get_json_response('/datastore/user/%s/list/'%user_2, self.DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to get valid data while logged in.')
        self.assertEqual(len(response['storage_objects']), len(transcription_list_2), 'Expected the newly added keys to match.')

        query_key = transcription_2.key.split(':')[1]
        response, status = self.get_json_response('/datastore/user/%s/list/%s'%(user_2,query_key), self.DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to get valid data while logged in.')

        query_key = response['storage_objects'][0]['id']
        response, status = self.get_json_response('/datastore/?store_id=%s'%query_key, self.DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to get valid data while logged in.')

        self.assertEqual(len(str(response['data'])), len(transcription_2.get_data()), 'Expected the queried data to match the other user's data.')
