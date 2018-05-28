from .helper_exports import datastore_export

from application.auth.required import auth_required
from application.datastore.views.export_by_user_key import ExportByUserKeyWrapper

class AlveoExportByUserKeyRoute(ExportByUserKeyWrapper):
    decorators = [auth_required]
    def _process_get(user_id, key, revision):
        return datastore_export(user_id=user_id, key=key, revision=revision)

export_by_user_key_route = AlveoExportByUserKeyRoute.as_view('/alveo/datastore/export/user:key')
