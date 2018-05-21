import sqlalchemy as sa
from sqlalchemy_continuum import make_versioned

from application import db

make_versioned()

class Datastore(db.Model):
    __versioned__ = {}

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

sa.orm.configure_mappers()
