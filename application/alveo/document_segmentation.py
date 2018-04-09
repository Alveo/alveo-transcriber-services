import pyalveo
import uuid

from application import app
from application.segmentation.audio_segmentor import segment_audio_data

def segment_document(document_id, aas_key):
    client = pyalveo.Client(api_url=app.config['ALVEO_API_URL'], api_key=aas_key, use_cache=False, update_cache=False, cache_dir=None)

    audio_data = None
    try:
        audio_data = client.get_document(document_id)
    except:
        pass

    if audio_data is None:
        return None

    return segment_audio_data(audio_data)
