from pyalveo import *
from flask import g

from application import app, db
from application.users.model import User
from application.misc.events import handle_api_event
from application.auth.required import auth_required

from application.datastore.model import Datastore

@auth_required
@handle_api_event("alveo", "retrieve")
def alveo_retrieve(storage_key, revision):
    return Datastore.query.filter(Datastore.key == storage_key).filter(Datastore.revision == revision).filter(Datastore.user_id == g.user.id).first()

@auth_required
@handle_api_event("alveo", "store")
def alveo_store(storage_key, storage_value):
    revision = "latest"
    model = Datastore.query.filter(Datastore.key == storage_key).filter(Datastore.revision == revision).filter(Datastore.user_id == g.user.id).first()

    if model is None:
        model = Datastore(storage_key, storage_value, revision, g.user)
        db.session.add(model)
    else:
        model.value = storage_value

    db.session.commit()

    return model 
