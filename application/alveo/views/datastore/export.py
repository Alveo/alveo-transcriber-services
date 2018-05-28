from .helper_exports import datastore_export

from application.auth.required import auth_required
from application.datastore.views.export import ExportWrapper

class AlveoExportRoute(ExportWrapper):
    decorators = [auth_required]
    def _processor_get(self, user_id, revision):
        return datastore_export(user_id=user_id, revision=revision)

export_route = AlveoExportRoute.as_view('/alveo/datastore/export')
