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

    def _processor_get(self, store_id, user_id):
        query = Datastore.query.filter(Datastore.id == store_id).first()

        if query is None:
            abort(404, 'No match for the provided id')

        user = User.query.filter(User.id == query.user_id).first()

        if not user.domain == DOMAIN:
            abort(
                403,
                'You don\'t have permission to read the storage of an external user')

        data = json.loads(query.get_value())
        original_author = query.versions[0].user
        revision_author = query.user

        return {
            'id': query.id,
            'key': query.key.split(':')[1],
            'revision': query.revision,
            'revision_count': query.versions.count(),
            'transcription': data,
            'annotations_total': len(data),
            'timestamp': str(query.timestamp),
            'author': {
                'original': {
                    'ats_id': original_author.id,
                    'domain': original_author.domain,
                    'remote_id': original_author.remote_id
                },
                'revision': {
                    'ats_id': revision_author.id,
                    'domain': revision_author.domain,
                    'remote_id': revision_author.remote_id
                }
            }
        }

    def _processor_post(self, key, value, storage_spec, revision=None):

        if key is None or len(key) < 2:
            abort(400, 'Key is invalid or too short')

        validate_data(value)

        key = '%s:%s' % (DOMAIN, key)

        model = Datastore.query.filter(
            Datastore.key == key).filter(
            Datastore.user_id == g.user.id).first()

        data = json.dumps(value)

        # We're not interested in letting the user
        #  have their own revision names in the Alveo
        #  module right now.
        revision = str(uuid.uuid4())

        if model is None:
            model = Datastore(key, data, storage_spec, revision, g.user)
            db.session.add(model)
        else:
            model.set_value(data)
            model.revision = revision
            model.storage_spec = storage_spec 

        db.session.commit()

        return {
            'id': model.id,
            'revision': model.revision
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
