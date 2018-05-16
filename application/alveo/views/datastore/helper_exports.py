import zipfile
import io
import json

from .helper_query import datastore_query

from flask import send_file

def datastore_export(user_id=None, key=None, revision=None):
    transcriptions = datastore_query(user_id=user_id, key=key, revision=revision)

    if transcriptions is None or len(transcriptions) == 0:
        abort(404, 'No documents available to export');

    archive = io.BytesIO()

    with zipfile.ZipFile(archive, mode='w') as zf:
        for transcription in transcriptions:
            data = {
                    'revision': transcription.revision,
                    'key': transcription.key.split(':')[1],
                    'domain': transcription.key.split(':')[0],
                    'transcription': transcription.get_data()
                }
            zf.writestr('%s_%s.json' % (transcription.id, transcription.revision), json.dumps(data))
    archive.seek(0)

    return { 
            'filename': '%s.zip' % user_id, 
            'mimetype': 'application/zip',
            'data': archive
        }
