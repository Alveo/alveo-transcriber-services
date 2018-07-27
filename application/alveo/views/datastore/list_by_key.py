from .helper_lists import datastore_list

from application.auth.required import auth_required
from application.datastore.view_wrappers.list_by_key import ListByKeyWrapper

from application import limiter


class AlveoListByKeyRoute(ListByKeyWrapper):
    decorators = [
        auth_required,
        limiter.limit("50 per minute"),
        limiter.limit("1000 per hour"),
        limiter.limit("5000 per day")
    ]

    def _processor_get(self, user_id, key):
        return datastore_list(user_id=user_id, key=key)


list_by_key_route = AlveoListByKeyRoute.as_view('/alveo/datastore/list/key')
