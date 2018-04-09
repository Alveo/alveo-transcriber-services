from application import db

# See: https://bitbucket.org/zzzeek/sqlalchemy/issues/3850/request-sqlite-json1-ext-support
# Support for JSON storage in sqlite (used in unit testing) coming, will double over for postgresql too
#from sqlalchemy import JSON

class CachedSegmentationResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alveo_id = db.Column(db.String(512), nullable=False, unique=True)
    #data = db.Column(JSON)
    data = db.Column(db.String)

    def __init__(self, alveo_id, data):
        self.alveo_id = alveo_id
        self.data = data

    def __repr__(self):
        return str(self.alveo_id)

    def __str__(self):
        return str(self.alveo_id)
