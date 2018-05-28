from .helper_lists import datastore_list

from application.auth.required import auth_required
from application.datastore.views.list_by_user_key import ListByUserKeyWrapper

class AlveoListByUserKeyRoute(ListByUserKeyWrapper):
    decorators = [auth_required]

    def _processor_get(self, user_id, key, revision):
        return datastore_list(user_id=user_id, key=key, revision=revision)

list_by_user_key_route = AlveoListByUserKeyRoute.as_view('/alveo/datastore/list/user:key')
