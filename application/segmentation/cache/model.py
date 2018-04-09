from application import db

# See: https://bitbucket.org/zzzeek/sqlalchemy/issues/3850/request-sqlite-json1-ext-support
# Support for JSON storage in sqlite (used in unit testing) coming, will double over for postgresql too
#from sqlalchemy import JSON

class CachedSegmentation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    storage_id = db.Column(db.String(512), nullable=False, unique=True)
    #data = db.Column(JSON)
    data = db.Column(db.String)

    def __init__(self, storage_id, data):
        self.storage_id = storage_id
        self.data = data

    def __repr__(self):
        return str(self.storage_id)

    def __str__(self):
        return str(self.storage_id)

def cache_result(document_id, result):
    if len(document_id) is 0:
        raise Exception("Attempting to store something to the cache without a valid document identifier")
    cached_result = CachedSegmentation(document_id, str(result))
    db.session.add(cached_result)
    db.session.commit()

def get_cached_result(document_id):
    result = CachedSegmentation.query.filter(CachedSegmentation.storage_id == document_id).first()
    if result is None:
        return None

    return jsonify(result.data)
