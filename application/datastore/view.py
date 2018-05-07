from flask import abort, request, jsonify
from flask.views import MethodView

from application.auth.required import auth_required
from application.misc.events import get_handler_for

class DatastoreAPI(MethodView):
    def get(self):
        storage_key = request.args.get('storage_key')
        revision = request.args.get('revision')
        api_domain = request.headers.get('X-Api-Domain')

        if storage_key is None:
            abort(400, "storage_key not provided")

        match = None
        if revision is None:
            revision = "latest" # TODO

        store = get_handler_for(api_domain, 'retrieve')

        if store is None:
            abort(404, "No store matches the specified domain");

        results = store.handle(storage_key, revision)

        if results is None:
            abort(404, "No data found for specified storage_key")

        return jsonify(
                    {
                        "revision": revision,
                        "data": results 
                    }
                )

    def post(self):
        data = request.get_json()
        storage_key = None
        storage_value = None
        api_domain = request.headers.get('X-Api-Domain')

        try:
            storage_key = data['storage_key']
            storage_value = data['storage_value']
        except:
            pass

        if storage_key is None:
            abort(400, "storage_key not provided")

        if storage_value is None:
            abort(400, "storage_value not provided")

        store = get_handler_for(api_domain, 'store')

        if store is None:
            abort(404, "No store matches the specified domain");

        result = store.handle(storage_key, storage_value)

        return jsonify(
                    {
                        "key": storage_key,
                        "revision": result.revision,
                    }
                )

datastore_api = auth_required(DatastoreAPI.as_view('datastore_api'))
