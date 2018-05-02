from flask import abort, request, jsonify
from flask.views import MethodView

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

        # Find the thing, match it, invoke it
        # match = ?

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

        # Find the thing, match it, invoke it

        return jsonify(
                    {
                        "key": storage_key,
                        "revision": "latest",
                    }
                )

datastore_api = DatastoreAPI.as_view('datastore_api')
