import json

from pyalveo import *
from flask import g

from application import app, db
from application.users.model import User
from application.misc.events import handle_api_event
from application.auth.required import auth_required

from application.datastore.model import Datastore

from struct import pack, unpack

@auth_required
@handle_api_event("alveo", "retrieve")
def alveo_retrieve(storage_key, revision):
    ref = Datastore.query.filter(Datastore.key == storage_key).filter(Datastore.revision == revision).filter(Datastore.user_id == g.user.id).first()

    if ref is None:
        return None

    return json.loads(ref.value.decode())

@auth_required
@handle_api_event("alveo", "store")
def alveo_store(storage_key, storage_value):
    revision = "latest"
    model = Datastore.query.filter(Datastore.key == storage_key).filter(Datastore.revision == revision).filter(Datastore.user_id == g.user.id).first()
    
    data = json.dumps(storage_value).encode()
    if model is None:
        model = Datastore(storage_key, data, revision, g.user)
        db.session.add(model)
    else:
        model.value = data

    db.session.commit()

    return model 
