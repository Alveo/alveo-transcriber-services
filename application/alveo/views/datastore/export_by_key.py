from .helper_exports import datastore_export

from application.auth.required import auth_required
from application.datastore.view_wrappers.export_by_key import ExportByKeyWrapper

from application import limiter


class AlveoExportByKeyRoute(ExportByKeyWrapper):
    decorators = [
        auth_required,
        limiter.limit("5 per minute"),
        limiter.limit("25 per hour"),
        limiter.limit("50 per day")
    ]

    def _process_get(self, user_id, key, revision):
        return datastore_export(user_id=user_id, key=key, revision=revision)


export_by_key_route = AlveoExportByKeyRoute.as_view(
    '/alveo/datastore/export/key')
