import datetime

from application import db
from application.datastore.model import Datastore
from application.jobs.types import JobTypes


class Job(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    external_id = db.Column(db.String(256), nullable=False)

    description = db.Column(db.String(512), nullable=False)

    status = db.Column(db.Integer(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')

    # Note that the datastore is not read-only, it is possible to edit via the API.
    #  Is this ideal?
    datastore_id = db.Column(db.Integer, db.ForeignKey('datastore.id'), nullable=True)
    datastore = db.relationship('Datastore')

    def __init__(self, external_id, description, user, datastore, status=None):
        self.external_id = external_id
        self.description = description
        if status is None:
            status = JobTypes.QUEUED
        if datastore is None:
            raise IOError("Datastore must not be null")
        self.status = status
        self.user = user
        self.datastore = datastore

    def complete(self, spec, result):
        self.datastore.spec = spec
        self.datastore.set_value(result)
        db.session.commit()