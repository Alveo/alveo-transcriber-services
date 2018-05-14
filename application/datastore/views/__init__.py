from .export_by_user_key import APIExportByUserKey
from .export_by_user import APIExportByUser
from .export_key import APIExportKey
from .list_by_user_key import APIListByUserKey
from .list_by_user import APIListByUser
from .list_key import APIListKey
from .list import APIList
from .manage import APIManage

# General
manage = APIManage.as_view('ds_manage')

# Export API
export_by_user_key = APIExportByUserKey.as_view('ds_api_export_by_user_key')
export_by_user = APIExportByUser.as_view('ds_api_export_by_user')
export_key = APIExportKey.as_view('ds_api_export_key')
export = APIList.as_view('ds_api_export')

# List API
list_by_user_key = APIListByUserKey.as_view('ds_api_list_by_user_key')
list_by_user = APIListByUser.as_view('ds_api_list_by_user')
list_key = APIListKey.as_view('ds_api_list_key')
list = APIList.as_view('ds_api_list')
