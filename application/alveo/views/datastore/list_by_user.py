from .helper_lists import datastore_list

from application.auth.required import auth_required
from application.datastore.views.list_by_user import ListByUserWrapper

class AlveoListByUserRoute(ListByUserWrapper):
    decorators = [auth_required]

    def _process_get(user_id, key, revision):
        return datastore_list(user_id=user_id, revision=revision)

list_by_user_route = AlveoListByUserRoute.as_view('/alveo/datastore/list/user')
