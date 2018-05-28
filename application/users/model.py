from application import db


class User(db.Model):
    """Provides a generalised User model for linking stored data.

    The expectation is that the User will be remotely authenticated against
    another API via some sort of credential that will be sent by the client
    via the headers during a request.

    If this class doesn't fulfill your requiremnets, for example:
      * When a local user is desirable
      * Missing a very important column that must absolutely be stored
      * Authenticating per-request is too expensive
    ..then building off of this User model through inheritence is recommended.

    This will allow for a more flexible approach while tailoring for your needs.

    """

    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(192), nullable=False)
    remote_id = db.Column(db.String(128), nullable=False)
    __table_args__ = (
        db.UniqueConstraint(
            'remote_id',
            'domain',
            name='_remote_user_uc'),
    )

    def __init__(self, remote_id, domain):
        """ Generate the User

        Args:
            remote_id: The user_id on the remote server
            domain: The domain identifier of the remote server
        """
        self.remote_id = remote_id
        self.domain = domain

    def __repr__(self):
        """ Represent the user more helpfully

        Returns:
            String such as 'User id 30 (379273@alveo)'

        """
        return 'User id %s (%s@%s)' % (self.id, self.remote_id, self.domain)

    def __str__(self):
        """ Represent the user more helpfully

        Returns:
            String such as 'User id 30 (379273@alveo)'

        """
        return 'User id %s (%s@%s)' % (self.id, self.remote_id, self.domain)
