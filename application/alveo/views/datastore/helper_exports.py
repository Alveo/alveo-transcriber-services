import zipfile
import io
import json

from flask import send_file

def datastore_export(user_id=None, key=None, revision=None):
    transcriptions = datastore_query(user_id=user_id, key=key, revision=revision)
    transcriptions = transcriptions['list']

    if transcriptions is None or len(transcriptions) == 0:
        abort(404, 'No documents available to export');

    archive = io.BytesIO()

    with zipfile.ZipFile(archive, mode='w') as zf:
        for doc in docs:
            data = {
                    'revision': doc.revision,
                    'key': doc.key,
                    'transcription': doc.get_data()
                    }
            zf.writestr('%s.json' % doc.key, json.dumps(data))
    archive.seek(0)

    user_id = str(g.user.remote_user_id).split(':')[1]

    return { 
            'filename': '%s.zip' % user_id, 
            'mimetype': 'application/zip',
            'data': archive
        }
