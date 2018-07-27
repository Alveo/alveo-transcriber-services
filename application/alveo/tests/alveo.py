import os
import json
import random
import uuid
import secrets

from application import db
from application.alveo.module import DOMAIN
from application.datastore.model import Datastore
from application.users.model import User
from application.misc.modules import get_module_metadata

from tests import ATSTests

ALVEO_API_KEY = None
ALVEO_API_URL = None
DEFAULT_HEADERS = None

TEST_STORAGE_SPEC_VERSION = "1.0-test"

alveo_metadata = get_module_metadata('alveo')

if alveo_metadata is None:
    raise Exception('Module not loaded in app configuration.')

ALVEO_API_URL = alveo_metadata['api_url']
ALVEO_API_KEY = os.environ.get('ALVEO_API_KEY', None)

if ALVEO_API_KEY is None:
    raise Exception(
        'ALVEO_API_KEY environment variable is not set. Cannot proceed.')

DEFAULT_HEADERS = {
    'X-Api-Key': ALVEO_API_KEY,
    'X-Api-Domain': 'app.alveo.edu.au'
}


class AlveoTests(ATSTests):
    def setUp(self):
        ATSTests.setUp(self)
        self.ALVEO_API_URL = ALVEO_API_URL
        self.DEFAULT_HEADERS = DEFAULT_HEADERS

    def generateTranscription(self, amount=None):
        if amount is None:
            amount = random.randint(3, 100)

        start = 0
        end = 0
        transcription = []
        for i in range(amount):
            start = end + random.uniform(0.3, 5)
            end = start + random.uniform(3, 7)
            annotation = {
                "start": start,
                "end": end,
                "speaker": str(random.randint(1, 1000)),
                "caption": str(uuid.uuid4())
            }
            transcription.append(annotation)

        return transcription

    def generateSamplePostData(self, key=None, fields=None):
        if key is None:
            key = str(uuid.uuid4())
        if fields is None:
            fields = random.randint(5, 15)

        data = {
            "key": key,
            "value": [],
            "storage_spec": TEST_STORAGE_SPEC_VERSION
        }

        data['value'] = self.generateTranscription(fields)

        return data

    def generateSampleAlveoData(self):
        self.createSampleData()

        for i in range(random.randint(7, 15)):
            username = secrets.token_hex(8)
            user = User(username, DOMAIN)

            for i in range(random.randint(3, 25)):
                datastore = Datastore(
                    '%s:%s' % (DOMAIN, uuid.uuid4()),
                    json.dumps(self.generateTranscription()),
                    TEST_STORAGE_SPEC_VERSION,
                    user
                )
                db.session.add(datastore)
            db.session.add(user)
        db.session.commit()
