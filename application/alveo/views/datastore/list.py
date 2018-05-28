from .helper_lists import datastore_list

from application.auth.required import auth_required
from application.datastore.views.list import ListWrapper

class AlveoListRoute(ListWrapper):
    decorators = [auth_required]

    def _process_get(user_id, key, revision):
        return datastore_list(user_id=user_id, revision=revision)

list_route = AlveoListRoute.as_view('/alveo/datastore/list')
