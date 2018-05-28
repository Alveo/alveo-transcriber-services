from .helper_lists import datastore_list

from application.auth.required import auth_required
from application.datastore.view_wrappers.list_by_user import ListByUserWrapper

from application import limiter

class AlveoListByUserRoute(ListByUserWrapper):
    decorators = [
            auth_required,
            limiter.limit("50 per minute"),
            limiter.limit("1000 per hour"),
            limiter.limit("5000 per day")
        ]

    def _processor_get(self, user_id, revision):
        return datastore_list(user_id=user_id, revision=revision)

list_by_user_route = AlveoListByUserRoute.as_view('/alveo/datastore/list/user')
