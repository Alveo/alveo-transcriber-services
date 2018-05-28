from .helper_lists import datastore_list

from application.auth.required import auth_required
from application.datastore.view_wrappers.list import ListWrapper

class AlveoListRoute(ListWrapper):
    decorators = [auth_required]

    def _processor_get(self, user_id, revision):
        return datastore_list(user_id=user_id, revision=revision)

list_route = AlveoListRoute.as_view('/alveo/datastore/list')
