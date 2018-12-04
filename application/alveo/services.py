import pyalveo
import uuid

from flask import abort

from application import app, redis_queue
from application.segmentation.audio_segmenter import segment_audio_data
from application.transcribers.gcloud.speech import transcribe
from application.misc.modules import get_module_metadata


def retrieve_doc_as_user(document_id, api_key):
    alveo_metadata = get_module_metadata("alveo")
    if alveo_metadata is None:
        abort(404, "Could not segment document. 'alveo' module not loaded")

    api_url = alveo_metadata['api_url']
    client = pyalveo.Client(
        api_url=api_url,
        api_key=api_key,
        use_cache=False,
        update_cache=False,
        cache_dir=None)

    audio_data = None
    try:
        audio_data = client.get_document(document_id)
    except BaseException:
        pass

    return audio_data

def segment_document(document_id, api_key):
    audio_data = retrieve_doc_as_user(document_id, api_key)
    if audio_data is None:
        return None

    return segment_audio_data(audio_data)

def transcribe_document(document_id, api_key):
    audio_data = retrieve_doc_as_user(document_id, api_key)
    if audio_data is None:
        return None

    #redis_queue.enqueue(transcribe, retrieve_doc_as_user(document_id, api_key))
    return {"OK": True, "Status": "In queue"}