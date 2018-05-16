import io
import json
import zipfile
import uuid

from .alveo import AlveoTests

class AlveoExportRoutesTests(AlveoTests):
    def testExport(self):
        DATA_AMOUNT = 10
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

        data, is_json, status = self.get_file_response('/datastore/export/', self.DEFAULT_HEADERS)
        self.assertEqual(200, status, 'Expected OK status when attempting to export valid data while logged in.')
        self.assertFalse(is_json, 'Expected streamed file data, not actual JSON response.')

        zip_archive = zipfile.ZipFile(io.BytesIO(data), "a", zipfile.ZIP_DEFLATED, False)
        archive_names = zip_archive.namelist()
        archive_data = zip_archive.namelist()
        self.assertEqual(len(archive_names),  DATA_AMOUNT+2, 'Expected same amount of exported as amount posted.')

        with zip_archive.open('%s_%s.json' % (response_1['id'], response_1['revision'])) as myfile:
            zip_json = json.loads(myfile.read())
            self.assertEqual(len(zip_json['transcription']), len(json.dumps(dataset_1['value'])))

        with zip_archive.open('%s_%s.json' % (response_2['id'], response_2['revision'])) as myfile:
            zip_json = json.loads(myfile.read())
            self.assertEqual(len(zip_json['transcription']), len(json.dumps(dataset_2['value'])))
