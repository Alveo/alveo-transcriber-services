import json

from pyalveo import *
from flask import g, abort, jsonify

from application import app, db
from application.users.model import User
from application.misc.events import handle_api_event

from application.datastore.model import Datastore

from struct import pack, unpack

@handle_api_event('alveo', 'datastore:get')
def alveo_retrieve(storage_key=None, revision='latest', user_id=None, download_type=None):
    response = None
    query = None

    if storage_key == None and user_id == None:
        abort(403, 'Must provide either (or both of) a storage key or user to query')

    if user_id == 'self':
        user_id = g.user.remote_user_id
    elif user_id is not None:
        user_id = 'alveo:' + user_id

    if storage_key is None:
        query = Datastore.query;
    else:
        query = Datastore.query.filter(Datastore.key == 'alveo:'+storage_key)

    if user_id is not None:
        user = User.query.filter(User.remote_user_id == user_id).first()

        if user is None:
            abort(404, 'No user matching that ID was found')

        query = query.filter(Datastore.user_id == user.id)

    if revision is not None:
        query = query.filter(Datastore.revision == revision)

    query = query.all()
    total_queries = len(query)

    if total_queries > 1:
        exports = []
        for datastore in query:
            exports.append(export_json(datastore, user_id))
        response = { 'exports': exports }
    elif total_queries == 1:
        response = export_json(datastore=query[0], user_id=user_id, append_data=True)
    else:
        abort(404, 'No matches based on provided parameters')

    return jsonify(response)

@handle_api_event('alveo', 'datastore:post')
def alveo_store(storage_key, storage_value):
    revision = 'latest'
    
    if storage_key is None or len(storage_key) < 2:
        abort(400, 'Key is invalid or too short')

    storage_key = 'alveo:'+storage_key

    model = Datastore.query.filter(Datastore.key == storage_key).filter(Datastore.revision == revision).filter(Datastore.user_id == g.user.id).first()
    
    data = json.dumps(storage_value)
    if model is None:
        model = Datastore(storage_key, data, revision, g.user)
        db.session.add(model)
    else:
        model.set_data(data)

    db.session.commit()

    return jsonify(export_json(model))

def export_json(datastore, user_id=None, append_data=False):
    export = {
            'id': datastore.key.split(":")[1],
            'revision': datastore.revision,
       }

    if append_data:
        export['data'] = json.loads(datastore.get_data())

    if user_id is not None and user_id is not g.user.remote_user_id:
        export['creator'] = datastore.user.remote_user_id

    return export 
