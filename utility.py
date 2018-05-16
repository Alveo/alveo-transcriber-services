import io
import urllib.request
import zipfile
import json

import click

from application import app, db
from application.datastore.model import Datastore
from application.users.model import User 

@click.group()
def cli():
    pass

@click.command()
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

@click.command()
@click.argument('path')
def dump_storage(path):
    archive = export_storage()

    with open(path, 'wb') as f_out:
        f_out.write(archive.getvalue())

@click.command()
@click.argument('url')
def push_storage(url):
    archive = export_storage()

    request = urllib.request.Request(url, data=archive)
    response = urllib.request.urlopen(request)
    print(response)

cli.add_command(init_db)
cli.add_command(dump_storage)
cli.add_command(push_storage)

if __name__ == '__main__':
    cli()

