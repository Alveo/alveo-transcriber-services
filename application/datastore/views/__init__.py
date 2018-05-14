from application.datastore.views.export_by_user_key import APIExportByUserKey
from application.datastore.views.export_by_user import APIExportByUser
from application.datastore.views.export_key import APIExportKey
from application.datastore.views.list_by_user_key import APIListByUserKey
from application.datastore.views.list_by_user import APIListByUser
from application.datastore.views.list_key import APIListKey
from application.datastore.views.list import APIList

export_by_user_key = APIExportByUserKey.as_view('ds_api_export_by_user_key')
export_by_user = APIExportByUser.as_view('ds_api_export_by_user')
export_key = APIExportKey.as_view('ds_api_export_key')
export = APIList.as_view('ds_api_export')
list_by_user_key = APIListByUserKey.as_view('ds_api_list_by_user_key')
list_by_user = APIListByUser.as_view('ds_api_list_by_user')
list_key = APIListKey.as_view('ds_api_list_key')
list = APIList.as_view('ds_api_list')
