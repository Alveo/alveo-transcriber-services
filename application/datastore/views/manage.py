from flask import abort, g, jsonify, request
from application.misc.event_router import EventRouter

class APIManage(EventRouter):
    def get(self):
        storage_id = request.args.get('storage_id')

        response = self.event("datastore:get").handle(
                storage_id=storage_id,
                user_id=g.user.id
            )
        return jsonify(response)

    def post(self):
        data = request.get_json()
        storage_key = None
        storage_value = None

        try:
            storage_key = data['storage_key']
            storage_value = data['storage_value']
        except:
            if storage_key is None:
                abort(400, "storage_key not provided or invalid")

            if storage_value is None:
                abort(400, "storage_value not provided or invalid")

        response = self.event("datastore:post").handle(
                storage_key=storage_key,
                storage_value=storage_value
            )
        return jsonify(response)
