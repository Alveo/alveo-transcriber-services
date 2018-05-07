import json

from pyalveo import *
from flask import g, abort

from application import app, db
from application.users.model import User
from application.misc.events import handle_api_event

from application.datastore.model import Datastore

from struct import pack, unpack

@handle_api_event("alveo", "retrieve")
def alveo_retrieve(storage_key, revision):
    if storage_key is None or len(storage_key) < 2:
        abort(400, "Key is invalid or too short")

    storage_key = "alveo:"+storage_key

    ref = Datastore.query.filter(Datastore.key == storage_key).filter(Datastore.revision == revision).filter(Datastore.user_id == g.user.id).first()

    if ref is None:
        return None

    return json.loads(ref.get_data())

@handle_api_event("alveo", "store")
def alveo_store(storage_key, storage_value):
    revision = "latest"
    
    if storage_key is None or len(storage_key) < 2:
        abort(400, "Key is invalid or too short")

    storage_key = "alveo:"+storage_key

    model = Datastore.query.filter(Datastore.key == storage_key).filter(Datastore.revision == revision).filter(Datastore.user_id == g.user.id).first()
    
    data = json.dumps(storage_value)
    if model is None:
        model = Datastore(storage_key, data, revision, g.user)
        db.session.add(model)
    else:
        model.set_data(data)

    db.session.commit()

    return model 
