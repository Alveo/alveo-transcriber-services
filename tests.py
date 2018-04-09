import os
import unittest
import json

from application import app, db

class TestCase(unittest.TestCase):
    def get_json_response(self, path):
        response = self.app.get(path)
        data = response.data.decode('utf8').replace("'", '"')
        return json.loads(data)

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.longMessage = True

        with app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def tearDown(self):
        pass

    def testCreation(self):
        response = self.get_json_response('/')
        self.assertEqual(404, response['code'])
        self.assertTrue('Resource not found' in response['description'])

if __name__ == '__main__':
    unittest.main()
