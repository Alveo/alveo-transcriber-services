import io
import json
import zipfile
import uuid

from application import db
from application.users.model import User
from application.datastore.model import Datastore

from application.alveo.module import DOMAIN
from .alveo import AlveoTests


class AlveoExportRoutesTests(AlveoTests):
    def testExport(self):
        DATA_AMOUNT = 10
        for i in range(int(DATA_AMOUNT / 2)):
            self.postRandomData(domain=DOMAIN)

        response_query, dataset_1 = self.postRandomData(True, domain=DOMAIN)
        response_1, status = response_query
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to post valid data while logged in.')

        for i in range(int(DATA_AMOUNT / 2)):
            self.postRandomData(domain=DOMAIN)

        response_query, dataset_2 = self.postRandomData(True, domain=DOMAIN)
        response_2, status = response_query
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to post valid data while logged in.')

        data, is_json, status = self.get_file_response(
            DOMAIN + '/datastore/export/', self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to export valid data while logged in.')
        self.assertFalse(
            is_json, 'Expected streamed file data, not actual JSON response.')

        zip_archive = zipfile.ZipFile(io.BytesIO(
            data), 'a', zipfile.ZIP_DEFLATED, False)
        archive_names = zip_archive.namelist()
        archive_data = zip_archive.namelist()
        self.assertEqual(len(archive_names), DATA_AMOUNT + 2,
                         'Expected same amount of exported as amount posted.')

        with zip_archive.open('%s.json' % dataset_1['key']) as myfile:
            zip_json = json.loads(myfile.read())
            self.assertEqual(len(zip_json['transcription']), len(
                json.dumps(dataset_1['value'])))

        with zip_archive.open('%s.json' % dataset_2['key']) as myfile:
            zip_json = json.loads(myfile.read())
            self.assertEqual(len(zip_json['transcription']), len(
                json.dumps(dataset_2['value'])))

    def testExportRateLimit(self):
        # Post some random data so we don't get a 404 on our export request
        self.postRandomData(domain=DOMAIN)

        rate_limit = 5

        for i in range(rate_limit - 1):
            data, is_json, status = self.get_file_response(
                DOMAIN + '/datastore/export/', self.DEFAULT_HEADERS)
            self.assertEqual(
                200,
                status,
                'Expected OK status when attempting to post valid data while logged in.')

        data, is_json, status = self.get_file_response(
            DOMAIN + '/datastore/export/', self.DEFAULT_HEADERS)
        self.assertEqual(
            429,
            status,
            'Expected to be rate limited after exceeding threshold')

    def testExportByKey(self):
        DATA_AMOUNT = 6
        KEY = str(uuid.uuid4())

        for i in range(int(DATA_AMOUNT / 2)):
            self.postRandomData(domain=DOMAIN)

        dataset_1 = self.generateSamplePostData(key=KEY)
        response_1, status = self.post_json_request(
            DOMAIN + '/datastore/', json.dumps(dataset_1), self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to post valid data while logged in.')

        for i in range(int(DATA_AMOUNT / 2)):
            self.postRandomData(domain=DOMAIN)

        dataset_2 = self.generateSamplePostData(key=KEY)
        response_2, status = self.post_json_request(
            DOMAIN + '/datastore/', json.dumps(dataset_2), self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to post valid data while logged in.')

        data, is_json, status = self.get_file_response(
            DOMAIN + '/datastore/export/%s' % (KEY), self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to export valid data while logged in.')
        self.assertFalse(
            is_json, 'Expected streamed file data, not actual JSON response.')

        zip_archive = zipfile.ZipFile(io.BytesIO(
            data), 'a', zipfile.ZIP_DEFLATED, False)
        archive_names = zip_archive.namelist()
        archive_data = zip_archive.namelist()
        self.assertEqual(len(archive_names), 1,
                         'Expected only the latest revision to be exported')

        with zip_archive.open('%s.json' % KEY) as myfile:
            zip_json = json.loads(myfile.read())
            self.assertEqual(len(zip_json['transcription']), len(
                json.dumps(dataset_2['value'])))

    # TODO Should we be able to export all revisions?

    def testOtherDomainExportFail(self):
        self.generateSampleAlveoData()

        user = User.query.filter(User.domain == DOMAIN).first()
        self.assertTrue(
            user is not None,
            'Expected sample users to exist from generated sample data.')

        # Change the user's domain
        user.domain = 'notalveo'
        db.session.commit()

        data, is_json, status = self.get_file_response(
            DOMAIN + '/datastore/user/%s/export/' %
            user.id, self.DEFAULT_HEADERS)
        self.assertEqual(
            403,
            status,
            'Expected forbidden status when attempting to list store from a different user on another domain, while logged in.')
        self.assertTrue(
            is_json, 'Expected JSON error message about not being accessible')

    def testOtherUserExport(self):
        self.generateSampleAlveoData()
        user = User.query.filter(User.domain == DOMAIN).first()

        self.assertTrue(
            user is not None,
            'Expected sample users to exist from generated sample data.')

        data, is_json, status = self.get_file_response(
            DOMAIN + '/datastore/user/%s/export/' %
            user.id, self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected OK status when attempting to export valid data from another user of the same module while logged in.')
        self.assertFalse(
            is_json, 'Expected streamed file data, not actual JSON response.')

        transcription_list = Datastore.query.filter(
            Datastore.user_id == user.id).all()

        zip_archive = zipfile.ZipFile(io.BytesIO(
            data), 'a', zipfile.ZIP_DEFLATED, False)
        archive_names = zip_archive.namelist()

        self.assertEqual(
            len(archive_names),
            len(transcription_list),
            'Expected same amount of exported transcriptions to what the other user has available.')
