from pyalveo import pyalveo, APIError
from flask import abort
from urllib.parse import urlparse

from application.misc.modules import get_module_metadata

def verify_access(remote_path, api_key):
        api_path = str(urlparse(remote_path).path)
        if '/' not in api_path or api_path == "/":
            abort(
                400,
                'Request did not include an Alveo document identifier to work with')

        # We care more about the user itself than the user_id, another option
        # is to query the database for something that matches the key but that
        # would be slower
        alveo_metadata = get_module_metadata("alveo")
        api_url = alveo_metadata['api_url']
        client = pyalveo.Client(
            api_url=api_url,
            api_key=api_key,
            use_cache=False,
            update_cache=False,
            cache_dir=None)

        # Check if we can access the list first.
        # Would be good if we could just check Alveo permissions instead of retrieving the item directly.
        # https://github.com/Alveo/pyalveo/issues/11
        try:
            item_path = remote_path.split('/document/')[0]
            client.get_item(item_path) # We just test for access
        except APIError as e:
            return False, str(e)

        return True, "200"