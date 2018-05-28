from .helper_exports import datastore_export

from application.auth.required import auth_required
from application.datastore.views.export_key import ExportByKeyWrapper

class AlveoExportByKeyRoute(ExportByKeyWrapper):
    decorators = [auth_required]
    def _process_get(self, user_id, key, revision):
        return datastore_export(user_id=user_id, key=key, revision=revision)

export_by_key_route = AlveoExportByKeyRoute.as_view('/alveo/datastore/export/key')
