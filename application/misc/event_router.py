from flask import abort, request
from flask.views import MethodView

from application.auth.required import auth_required
from application.misc.events import get_handler_for

class EventRouter(MethodView):
    def event(self, event_id):
        api_domain = request.headers.get('X-Api-Domain')

        handler = get_handler_for(api_domain, event_id)

        if handler is None:
            abort(404, "No handler matches the specified X-Api-Domain");

        return handler
