import pyalveo
import uuid

from application import app
from application.segmentation.audio_segmentor import segment_audio_data
from application.misc.events import get_module_metadata

def segment_document(document_id, api_key):
    alveo_metadata = get_module_metadata("alveo")
    if alveo_metadata is None:
        abort(404, "Could not segment document. 'alveo' module not loaded")

    api_url = alveo_metadata['api_url']
    client = pyalveo.Client(api_url=api_url, api_key=api_key, use_cache=False, update_cache=False, cache_dir=None)

    audio_data = None
    try:
        audio_data = client.get_document(document_id)
    except:
        pass

    if audio_data is None:
        return None

    return segment_audio_data(audio_data)
