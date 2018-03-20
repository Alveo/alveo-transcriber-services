from application import db

class CachedSegmentationResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(512), nullable=False, unique=True)
    data = db.Column(db.String, nullable=False)

    def __init__(self, identifier, data):
        self.identifier = identifier
        self.data = data

    def __repr__(self):
        return str(self.identifier)

    def __str__(self):
        return str(self.identifier)
