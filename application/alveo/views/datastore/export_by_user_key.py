from .helper_exports import datastore_export

from application.auth.required import auth_required
from application.datastore.view_wrappers.export_by_user_key import ExportByUserKeyWrapper

from application import limiter


class AlveoExportByUserKeyRoute(ExportByUserKeyWrapper):
    decorators = [
        auth_required,
        limiter.limit("5 per minute"),
        limiter.limit("25 per hour"),
        limiter.limit("50 per day")
    ]

    def _process_get(self, user_id, key):
        return datastore_export(user_id=user_id, key=key)


export_by_user_key_route = AlveoExportByUserKeyRoute.as_view(
    '/alveo/datastore/export/user:key')
