from .alveo import AlveoTests

from application.alveo.module import DOMAIN


class AlveoSegmentationTests(AlveoTests):
    def testSegmentationNoAuth(self):
        response, status = self.get_json_response(DOMAIN + '/segment')
        self.assertEqual(
            401,
            status,
            'Expected unauthorised status when attempting to segment without logging in.')

    def testSegmentationAuthNoDoc(self):
        response, status = self.get_json_response(
            DOMAIN + '/segment?remote_url=' + self.ALVEO_API_URL, self.DEFAULT_HEADERS)
        self.assertTrue(
            'Alveo document identifier' in response['description'],
            'Expected error to be about the missing Alveo document identifier when authorised, attempting to segment without a document identifier.')
        self.assertEqual(
            400,
            status,
            'Expected bad request status when attempting to segment without a document (via header).')

    def testSegmentationInvalidDocument(self):
        invalid_remote_url = 'https://app.alveo.edu.au/catalog/doesnot/exist.wav'
        response, status = self.get_json_response(
            DOMAIN + '/segment?remote_url=' + invalid_remote_url, self.DEFAULT_HEADERS)
        self.assertTrue(
            'not-found' in response['description'],
            'Expected error to be about an inaccessible Alveo document identifier when attempting to segment with an invalid document identifier.')
        self.assertEqual(
            400,
            status,
            'Expected bad request status when attempting to segment an invalid document.')

    def testSegmentationValidDocument(self):
        remote_url = 'https://app.alveo.edu.au/catalog/austalk/1_1274_2_7_001/document/1_1274_2_7_001-ch6-speaker16.wav'

        response, status = self.get_json_response(
            DOMAIN + '/segment?remote_url=' + remote_url, self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected status OK when attempting to segment a valid document.')
        self.assertTrue(len(response['results']) > 0,
                        'Expected a list of segments when segmenting a valid document.')
        results = response['results']

        response, status = self.get_json_response(
            DOMAIN + '/segment?remote_url=' + remote_url, self.DEFAULT_HEADERS)
        self.assertEqual(
            200,
            status,
            'Expected status OK when attempting to segment a valid document, again (cache check).')
        self.assertTrue(
            len(
                response['results']) > 0,
            'Expected a list of segments when segmenting a valid document, again (cache check).')
        cached_results = response['results']

        self.assertTrue(
            len(results) is len(cached_results),
            'Expected the original segmentation results to match the number of cached segmentation results when segmenting twice.')
