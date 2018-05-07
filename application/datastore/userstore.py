from flask import abort, request
from flask.views import MethodView

from application.auth.required import auth_required
from application.misc.events import get_handler_for

class UserstoreAPI(MethodView):
    def get(self):
        api_domain = request.headers.get('X-Api-Domain')

        store = get_handler_for(api_domain, 'userstore_archive')

        if store is None:
            abort(404, "No store matches the specified domain");

        return store.handle()

userstore_api = auth_required(UserstoreAPI.as_view('userstore_api'))
