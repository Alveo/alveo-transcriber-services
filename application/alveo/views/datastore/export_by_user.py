from application.alveo.views.datastore.helper_exports import datastore_export

from application.auth.required import auth_required
from application.datastore.view_wrappers.export_by_user import ExportByUserWrapper

from application import limiter


class AlveoExportByUserRoute(ExportByUserWrapper):
    decorators = [
        auth_required,
        limiter.limit("10 per minute"),
        limiter.limit("40 per hour"),
        limiter.limit("200 per day")
    ]

    def _processor_get(self, user_id):
        return datastore_export(user_id=user_id)


export_by_user_route = AlveoExportByUserRoute.as_view(
    '/alveo/datastore/export/user')
