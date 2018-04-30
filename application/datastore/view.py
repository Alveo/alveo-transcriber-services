from flask import g, abort, request, jsonify
from flask.views import MethodView

from application import db
from application.datastore.model import Datastore

from application.auth.auth_handler import auth_required

class DatastoreAPI(MethodView):
    @auth_required
    def get(self):
        storage_key = request.args.get('storage_key')
        revision = request.args.get('revision')

        if storage_key is None:
            abort(400, "storage_key not provided")

        match = None
        if revision is None:
            revision = "latest" # TODO

        match = Datastore.query.filter(Datastore.key == storage_key).filter(Datastore.revision == revision).filter(Datastore.user_id == g.user.id).first()

        if match is None:
            abort(404, "No matches found");

        return jsonify(
                    {
                        "results": match.value
                    }
                )


    @auth_required
    def post(self):
        data = request.get_json()
        storage_key = None
        storage_value = None

        try:
            storage_key = data['storage_key']
            storage_value = data['storage_value']
        except:
            pass

        if storage_key is None:
            abort(400, "storage_key not provided")

        if storage_value is None:
            abort(400, "storage_value not provided")

        revision = "latest"
        match = Datastore.query.filter(Datastore.key == storage_key).filter(Datastore.revision == revision).filter(Datastore.user_id == g.user.id).first()

        if match is None:
            storage_model = Datastore(storage_key, storage_value, revision, g.user)
            db.session.add(storage_model)
        else:
            match.value = storage_value

        db.session.commit()

        return jsonify(
                    {
                        "key": storage_key,
                        "revision": "latest",
                    }
                )

datastore_api = DatastoreAPI.as_view('datastore_api')
