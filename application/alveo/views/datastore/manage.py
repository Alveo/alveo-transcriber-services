import json

from pyalveo import *
from flask import g, abort

from application import db
from application.users.model import User
from application.misc.events import handle_api_event

from application.datastore.model import Datastore

from application.alveo.module import DOMAIN, SUPPORTED_STORAGE_KEYS

@handle_api_event('alveo', 'datastore:get')
def alveo_retrieve(store_id, user_id):
    query = Datastore.query.filter(Datastore.id == store_id).first()

    if query is None:
        abort(404, 'No match for the provided id')

    user = User.query.filter(User.id == query.user_id).first()

    if not user.domain == DOMAIN:
        abort(403, 'You don\'t have permission to read the storage of an external user')

    return {
            'id': query.id,
            'key': query.key.split(':')[1],
            'revision': query.revision,
            'data': json.loads(query.get_value()),
            'creator': query.user_id
        }

@handle_api_event('alveo', 'datastore:post')
def alveo_store(key, value, revision=None):
    if revision == None:
        revision = 'latest' # TODO generate
    
    if key is None or len(key) < 2:
        abort(400, 'Key is invalid or too short')

    validate_data(value)

    key = '%s:%s' % (DOMAIN, key)

    model = Datastore.query.filter(Datastore.key == key).filter(Datastore.revision == revision).filter(Datastore.user_id == g.user.id).first()
    
    data = json.dumps(value)

    if model is None:
        model = Datastore(key, data, revision, g.user)
        db.session.add(model)
    else:
        # We could abort because a PUT request should be used, but should we?
        # TODO Maybe this should be explored after proper revisioning is in, as
        #  we in theory shouldn't be editing existing revisions anyway.
        #  abort(400, 'A match for this key and revision already exists')
        model.set_value(data)

    db.session.commit()

    return {
            'id': model.id,
            'revision': model.revision
        }

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
                abort(400, 'Invalid type for key \'%s\', expected %s got %s' % (key, expected_type.__name__, type(entry[key]).__name__))

        for key in supported_keys:
            if SUPPORTED_STORAGE_KEYS[key]['required']:
                if key not in keys:
                    abort(400, 'Required key is missing: %s' % key)
