import os
import unittest

os.environ['ATS_ENVIRONMENT'] = 'application.config.TestEnvironment'

from application import app, db

try:
    from application.alveo.tests import *
except Exception as e:
    print("Skipping Alveo tests. Reason: ", e)

class MainTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
