import zipfile
import io

from flask import g, send_file, jsonify

from application.misc.events import handle_api_event
from application.datastore.model import Datastore

@handle_api_event("alveo", "userstore_list")
def alveo_userstore_list():
    transcriptions = Datastore.query.filter(Datastore.user_id == g.user.id).all()

    response_transcriptions = []
    for transcription in transcriptions:
        response_transcriptions.append(
                {
                    'id': transcription.key,
                    'annotation_count': len(transcription.get_data())
                }
            )

    return jsonify(response_transcriptions)

@handle_api_event("alveo", "userstore_list_all")
def alveo_userstore_list_all(key):
    transcriptions = Datastore.query.filter(Datastore.key == key).all()

    response_transcriptions = []
    for transcription in transcriptions:
        response_transcriptions.append(
                {
                    'id': transcription.key,
                    'creator': transcription.user.remote_user_id,
                    'annotation_count': len(transcription.get_data())
                }
            )

    return jsonify(response_transcriptions)
