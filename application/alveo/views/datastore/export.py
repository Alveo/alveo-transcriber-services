from .helper_exports import datastore_export

from application.auth.required import auth_required
from application.datastore.view_wrappers.export import ExportWrapper

from application import limiter


class AlveoExportRoute(ExportWrapper):
    decorators = [
        auth_required,
        limiter.limit("5 per minute"),
        limiter.limit("25 per hour"),
        limiter.limit("50 per day")
    ]

    def _processor_get(self, user_id):
        return datastore_export(user_id=user_id)


export_route = AlveoExportRoute.as_view('/alveo/datastore/export')
