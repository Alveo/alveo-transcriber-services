from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(48), nullable=False, unique=True)

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return str(self.user_id)

    def __str__(self):
        return str(self.user_id)
