import io
import urllib.request
import zipfile
import json

import click

from application import app, db
from application.datastore.model import Datastore

@click.group()
def cli():
    pass

@click.command()
def init_db():
    db.drop_all()
    db.create_all()
    click.echo("Database has been rebuilt.")

@click.command()
@click.argument('url')
def push_transcriptions(url):
    data = Datastore.query.all()

    archive = io.BytesIO()
    with zipfile.ZipFile(archive, mode='w') as zf:
        for transcription in data:
            data = {
                    "id": transcription.key,
                    "creator": transcription.user.remote_user_id,
                    "revision": transcription.revision,
                    "transcription": transcription.value.decode()
                    }
            zf.writestr('%s.json' % transcription.key, json.dumps(data))
    archive.seek(0)

    request = urllib.request.Request(url, data=archive)
    response = urllib.request.urlopen(request)
    print(response)

cli.add_command(init_db)
cli.add_command(push_transcriptions)

if __name__ == '__main__':
    cli()

