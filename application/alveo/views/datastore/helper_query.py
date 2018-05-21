from flask import abort

from application.datastore.model import Datastore
from application.users.model import User 

from application.alveo.module import DOMAIN

def datastore_query(user_id=None, key=None, revision=None):
    query = None

    if key is None:
        query = Datastore.query;
    else:
        query = Datastore.query.filter(Datastore.key == '%s:%s' % (DOMAIN, key))

    if user_id is not None:
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            abort(404, "User not found")

        if not user.domain == DOMAIN:
            abort(403, "You don't have permission to view external users")
        query = query.filter(Datastore.user_id == user_id)

    if revision != None:
        query = query.filter(Datastore.revision == revision)

    return query.all()
