import zipfile
import io
import json

from .helper_query import datastore_query

from flask import abort


def datastore_export(user_id=None, key=None):
    transcriptions = datastore_query(
        user_id=user_id, key=key)

    if transcriptions is None or len(transcriptions) == 0:
        abort(404, 'No documents available to export')

    archive = io.BytesIO()

    with zipfile.ZipFile(archive, mode='w') as zf:
        for transcription in transcriptions:
            data = {
                'timestamp': str(transcription.timestamp),
                'author': {
                    'original': str(transcription.versions[0].user),
                    'editor': str(transcription.user)
                },
                'remote_id': transcription.id,
                'domain': transcription.key.split(':')[0],
                'transcription': json.dumps(transcription.get_value()),
                'storage_spec': stranscription.storage_spec,
                'version': transcription.version
            }
            zf.writestr(
                '%s.json' %
                transcription.key.split(':')[1],
                json.dumps(data))
    archive.seek(0)

    return {
        'filename': '%s.zip' % user_id,
        'mimetype': 'application/zip',
        'data': archive
    }
