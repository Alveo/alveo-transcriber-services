import json

from pyalveo import *
from flask import g, abort, jsonify

from application import db
from application.users.model import User
from application.misc.events import handle_api_event

from application.datastore.model import Datastore

from . import DOMAIN

@handle_api_event('alveo', 'datastore:get')
def alveo_retrieve(storage_id, user_id):
    query = Datastore.query.filter(Datastore.id == storage_id).first()

    if query is None:
        abort(404, "No match for the provided id")

    user = User.query.filter(User.id == query.user_id).first()

    if not user.domain == DOMAIN:
        abort(403, "You don't have permission to read the storage of an external user")

    return {
            'id': query.id,
            'revision': query.revision,
            'data': json.loads(query.get_data()),
            'creator': query.user_id
        }

@handle_api_event('alveo', 'datastore:post')
def alveo_store(storage_key, storage_value):
    revision = 'latest'
    
    if storage_key is None or len(storage_key) < 2:
        abort(400, 'Key is invalid or too short')

    storage_key = '%s:%s' % (DOMAIN, storage_key)

    model = Datastore.query.filter(Datastore.key == storage_key).filter(Datastore.revision == revision).filter(Datastore.user_id == g.user.id).first()
    
    data = json.dumps(storage_value)
    if model is None:
        model = Datastore(storage_key, data, revision, g.user)
        db.session.add(model)
    else:
        model.set_data(data)

    db.session.commit()

    return {
            'id': model.id,
            'revision': model.revision
        }
