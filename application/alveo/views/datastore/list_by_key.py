from .helper_lists import datastore_list

from application.auth.required import auth_required
from application.datastore.view_wrappers.list_by_key import ListByKeyWrapper

class AlveoListByKeyRoute(ListByKeyWrapper):
    decorators = [auth_required]

    def _processor_get(self, user_id, key, revision):
        return datastore_list(user_id=user_id, key=key, revision=revision)

list_by_key_route = AlveoListByKeyRoute.as_view('/alveo/datastore/list/key')
