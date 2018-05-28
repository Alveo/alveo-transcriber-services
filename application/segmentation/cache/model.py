import json

from application import db


class CachedSegmentation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    storage_id = db.Column(db.String(512), nullable=False, unique=True)
    data = db.Column(db.LargeBinary)

    def __init__(self, storage_id, data):
        self.storage_id = storage_id
        self.data = data.encode()

    def get_json(self):
        return json.loads(self.data.decode())

    def __repr__(self):
        return str(self.storage_id)

    def __str__(self):
        return str(self.storage_id)


def cache_result(document_id, result):
    if len(document_id) is 0:
        raise Exception(
            "Attempting to store something to the cache without a valid document identifier")
    db.session.add(CachedSegmentation(document_id, json.dumps(result)))
    db.session.commit()


def get_cached_result(document_id):
    result = CachedSegmentation.query.filter(
        CachedSegmentation.storage_id == document_id).first()
    if result is None:
        return None

    return result.get_json()
