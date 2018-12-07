import datetime

from application import db
from application.datastore.model import Datastore
from application.jobs.types import JobTypes


class Job(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    external_id = db.Column(db.String(256), nullable=False)

    status = db.Column(db.Integer(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')

    datastore_id = db.Column(db.Integer, db.ForeignKey('datastore.id'), nullable=False)
    datastore = db.relationship('Datastore')

    def __init__(self, external_id, status, user, datastore):
        self.external_id = external_id
        if status is None:
            status = JobTypes.QUEUED
        self.status = status
        self.user = user
        self.datastore = datastore

    def complete(self, spec, result):
        self.datastore.spec = spec
        self.datastore.set_value(result)
        db.session.commit()