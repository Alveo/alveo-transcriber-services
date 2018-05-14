from flask import abort

from application.datastore.model import Datastore
from application.users.model import User 

def datastore_list(user_id=None, key=None, revision=None):
    response = None
    query = None

    if revision is None:
        revision = "latest"

    if key is None:
        query = Datastore.query;
    else:
        query = Datastore.query.filter(Datastore.key == 'alveo:'+key)

    if user_id is not None:
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            abort(404, "User not found")

        if user.remote_user_id.startswith("alveo"):
            query = query.filter(Datastore.user_id == user_id)
        else:
            abort(403, "You don't have permission to view external users")

    if revision != "any":
        query = query.filter(Datastore.revision == revision)


    query = query.all()
    data = {
                'revision': revision,
                'list': query
        }

    return data
