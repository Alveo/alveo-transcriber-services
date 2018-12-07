import datetime
import sqlalchemy as sa
from sqlalchemy_continuum import make_versioned

from application import db

make_versioned()


class Datastore(db.Model):
    __versioned__ = {}

    id = db.Column(db.Integer(), primary_key=True)

    key = db.Column(db.String(256), nullable=False)
    value = db.Column(db.LargeBinary, nullable=False)

    storage_spec = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    alias = db.Column(db.String(256), nullable=False)
    __table_args__ = (
        db.UniqueConstraint(
            'key',
            'user_id',
            name='_key_user_uc'),
    )

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')

    def __init__(self, key, value, storage_spec, user, alias):
        self.key = key
        self.set_value(value)
        self.storage_spec = storage_spec 
        self.user = user
        self.alias = alias

    def set_value(self, value):
        self.value = value.encode()

    def get_value(self):
        return self.value.decode()


sa.orm.configure_mappers()
