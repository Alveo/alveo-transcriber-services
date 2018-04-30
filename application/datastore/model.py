from application import db

class Datastore(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    key = db.Column(db.String(256), nullable=False)
    value = db.Column(db.String, nullable=False)
    revision = db.Column(db.String(64), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')

    def __init__(self, key, value, revision, user):
        self.key = key
        self.value = value
        self.revision = revision

        self.user = user
