from application import app, db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    remote_user_id = db.Column(db.String(48), nullable=False, unique=True)

    def __init__(self, remote_user_id):
        self.remote_user_id = remote_user_id

    def __repr__(self):
        return str(self.remote_user_id)

    def __str__(self):
        return str(self.remote_user_id)
