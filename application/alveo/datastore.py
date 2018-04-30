from pyalveo import *
from flask import g

from application import app, db
from application.users.model import User
from application.datastore.handler import register_datastore_read, register_datastore_write

from application.datastore.model import Datastore

@register_datastore_read("alveo")
def datastore_read_alveo(storage_key, revision):
    return Datastore.query.filter(Datastore.key == storage_key).filter(Datastore.revision == revision).filter(Datastore.user_id == g.user.id).first()

@register_datastore_write("alveo")
def datastore_write_alveo(storage_key, storage_value):
    revision = "latest"
    match = Datastore.query.filter(Datastore.key == storage_key).filter(Datastore.revision == revision).filter(Datastore.user_id == g.user.id).first()

    if match is None:
        storage_model = Datastore(storage_key, storage_value, revision, g.user)
        db.session.add(storage_model)
    else:
        match.value = storage_value

    db.session.commit()
