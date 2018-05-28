from .helper_exports import datastore_export

from application.auth.required import auth_required
from application.datastore.views.export_by_user import ExportByUserWrapper

class AlveoExportByUserRoute(ExportByUserWrapper):
    decorators = [auth_required]
    def _process_get(user_id, revision):
        return datastore_export(user_id=user_id, revision=revision)

export_by_user_route = AlveoExportByUserRoute.as_view('/alveo/datastore/export/user')
