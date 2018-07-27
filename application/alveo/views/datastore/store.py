import json
import uuid

from pyalveo import *
from flask import g, abort

from application import db
from application.users.model import User

from application.datastore.model import Datastore

from application.alveo.module import DOMAIN, SUPPORTED_STORAGE_KEYS

from application.auth.required import auth_required
from application.datastore.view_wrappers.store import StoreWrapper

from application import limiter


class AlveoStoreRoute(StoreWrapper):
    decorators = [
        auth_required,
        limiter.limit("250 per minute"),
        limiter.limit("10000 per hour"),
        limiter.limit("60000 per day")
    ]

    def _processor_get(self, object_id, user_id=None, version=None):
        query = Datastore.query.filter(Datastore.id == object_id).first()

        if query is None:
            abort(404, 'No match for the provided id')

        user = User.query.filter(User.id == query.user_id).first()

        if not user.domain == DOMAIN:
            abort(
                403,
                'You don\'t have permission to read the storage of an external user')

        if version != None:
            try:
                query = query.versions[version]
            except:
                abort(404, 'Version doesn\'t exist for provided id')

        data = json.loads(query.get_value())
        original_author = query.versions[0].user
        version_author = query.user

        return {
            'id': query.id,
            'key': query.key.split(':')[1],
            'version': version,
            'total_versions': query.versions.count(),
            'transcription': data,
            'annotations_total': len(data),
            'timestamp': str(query.timestamp),
            'author': {
                'original': {
                    'ats_id': original_author.id,
                    'domain': original_author.domain,
                    'remote_id': original_author.remote_id
                },
                'version': {
                    'ats_id': version_author.id,
                    'domain': version_author.domain,
                    'remote_id': version_author.remote_id
                }
            }
        }

    def _processor_post(self, key, value, storage_spec):

        if key is None or len(key) < 2:
            abort(400, 'Key is invalid or too short')

        validate_data(value)

        key = '%s:%s' % (DOMAIN, key)

        model = Datastore.query.filter(
            Datastore.key == key).filter(
            Datastore.user_id == g.user.id).first()

        data = json.dumps(value)

        if model is None:
            model = Datastore(key, data, storage_spec, g.user)
            db.session.add(model)
        else:
            model.set_value(data)
            model.storage_spec = storage_spec 

        db.session.commit()

        return {
            'id': model.id,
        }


store_route = AlveoStoreRoute.as_view('/alveo/datastore/')


def validate_data(data):
    if not isinstance(data, list):
        abort(400, 'Expected a list of JSON objects as the data type')

    supported_keys = SUPPORTED_STORAGE_KEYS.keys()

    for entry in data:
        keys = entry.keys()
        for key in keys:
            if key not in supported_keys:
                abort(400, 'Invalid/unsupported key \'%s\'' % key)

            expected_type = SUPPORTED_STORAGE_KEYS[key]['type']
            if not isinstance(entry[key], expected_type):
                abort(400, 'Invalid type for key \'%s\', expected %s got %s' %
                      (key, expected_type.__name__, type(entry[key]).__name__))

        for key in supported_keys:
            if SUPPORTED_STORAGE_KEYS[key]['required']:
                if key not in keys:
                    abort(400, 'Required key is missing: %s' % key)
