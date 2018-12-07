import pyalveo
import uuid
from datetime import datetime

from flask import abort
from rq import get_current_job

from application import app, db, redis_queue
from application.asr.engines.gcloud.speech import transcribe
from application.segmentation.audio_segmenter import segment_audio_data
from application.jobs.types import JobTypes
from application.jobs.model import Job
from application.misc.modules import get_module_metadata

from google.cloud.speech import enums

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
    try:
        active_job = get_current_job()
        job = Job.query.filter(Job.external_id == active_job.id).first()
        if job is None:
            print("Error: Job %s doesn't exist in application database" % active_job.id)
            return

        job.status = JobTypes.EXECUTING
        db.session.commit()

        audio_data = retrieve_doc_as_user(document_id, api_key)
        if audio_data is None:
            # Fail job
            job.status = JobTypes.FAILED
            job.description += "\n\n ERROR: %s could not be retrieved" % document_id
            db.session.delete(job.datastore)
            job.datastore = None
            db.session.commit()
            return

        params = {
            'audio_data': audio_data,
            'timeout': 18000,
            'audio_duration': 61,
            'sample_rate_hertz': 16000,
            'language_code': 'en-AU',
            'storage_bucket': app.config['GCLOUD_STORAGE_BUCKET'],
            'encoding': enums.RecognitionConfig.AudioEncoding.LINEAR16,
            'enable_word_time_offsets': True
        }

        tra = transcribe(params)
        # TODO process the transcription into something more usable

        transcription = tra

        job.status = JobTypes.FINISHED
        job.datastore.timestamp = datetime.now()
        job.datastore.set_value(transcription)
        job.datastore.alias = "ready"
        db.session.commit()

    except Exception as e:
        job.status = JobTypes.FAILED
        job.description += "\n\n ERROR: Internal backend error"
        db.session.delete(job.datastore)
        job.datastore = None
        db.session.commit()
        raise(e)
