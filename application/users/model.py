from application import app, db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(192), nullable=False)
    remote_id = db.Column(db.String(128), nullable=False)

    def __init__(self, remote_id, domain):
        self.remote_id = remote_id
        self.domain = domain
        # TODO prevent duplicates

    def __repr__(self):
        return 'User id %s (%s@%s)' % (self.id, self.remote_id, self.domain)

    def __str__(self):
        return 'User id %s (%s@%s)' % (self.id, self.remote_id, self.domain)
