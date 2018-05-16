import os
import random
import uuid

from application.misc.events import get_module_metadata
from tests import ATSTests

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

class AlveoTests(ATSTests):
    def setUp(self):
        ATSTests.setUp(self)
        self.ALVEO_API_URL = ALVEO_API_URL
        self.DEFAULT_HEADERS = DEFAULT_HEADERS

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
