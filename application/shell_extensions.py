import io
import requests
import os
import zipfile
import json

from application import app, db
from application.users.model import User 
from application.datastore.model import Datastore

import click
from flask_migrate import MigrateCommand
from flask.cli import AppGroup

extensions = AppGroup('app')

@extensions.command()
def init_db():
    db.drop_all()
    db.create_all()
    click.echo('Database has been rebuilt.')

def export_storage():
    datastore = Datastore.query.all()
    archive = io.BytesIO()

    with zipfile.ZipFile(archive, mode='w') as zf:
        for data in datastore:
            user = User.query.filter(data.user.id == User.id).first()
            entry = {
                    'id': data.key,
                    'creator': {
                            'local_id': user.id,
                            'remote_id': user.remote_id,
                            'domain': user.domain
                        },
                    'revision': data.revision,
                    'transcription': json.loads(data.get_data())
                    }
            zf.writestr('%s.json' % data.key, json.dumps(entry, indent=4))
    archive.seek(0)

    return archive

@extensions.command()
@click.argument('path')
def dump_storage(path):
    archive = export_storage()

    with open(path, 'wb') as f_out:
        f_out.write(archive.getvalue())

@extensions.command()
@click.argument('url')
def push_storage(url):
    archive = export_storage()
    headers = os.environ.get("ATS_PUSH_HEADERS", None)
    if headers is not None:
        headers = json.loads(headers)

    request = requests.post(url, files={'file': archive}, headers=headers)

    print(request)


app.cli.add_command(extensions)

