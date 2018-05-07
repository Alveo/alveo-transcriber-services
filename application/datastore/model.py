from application import db

class Datastore(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    key = db.Column(db.String(256), nullable=False)
    value = db.Column(db.LargeBinary, nullable=False)
    revision = db.Column(db.String(64), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')

    def __init__(self, key, value, revision, user):
        self.key = key
        self.set_data(value)
        self.revision = revision

        self.user = user

    def set_data(self, value):
        self.value = value.encode()

    def get_data(self):
        return self.value.decode()
