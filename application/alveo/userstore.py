import zipfile
import io
import json

from flask import g, send_file

from application.misc.events import handle_api_event
from application.datastore.model import Datastore

@handle_api_event("alveo", "userstore_archive")
def alveo_retrieve():
    docs = Datastore.query.filter(Datastore.user_id == g.user.id).all()

    if docs is None or len(docs) == 0:
        abort(400, "No documents associated with user");

    archive = io.BytesIO()

    with zipfile.ZipFile(archive, mode='w') as zf:
        for doc in docs:
            data = {
                    "revision": doc.revision,
                    "transcription": doc.value.decode()
                    }
            zf.writestr(doc.key, json.dumps(data))
    archive.seek(0)

    user_id = str(g.user.remote_user_id).split(':')[1]

    return send_file(
        archive,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='%s.zip' % user_id)
