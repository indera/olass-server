"""
ORM for 'oauth_access_token' table

"""
from olass.models.crud_mixin import CRUDMixin
from olass.models.oauth_client_entity import OauthClientEntity
from olass import utils
from olass.main import db
from datetime import datetime

"""
+---------------+--------------+------+-----+---------+----------------+
| Field         | Type         | Null | Key | Default | Extra          |
+---------------+--------------+------+-----+---------+----------------+
| id            | int(11)      | NO   | PRI | NULL    | auto_increment |
| client_id     | varchar(40)  | NO   | MUL | NULL    |                |
| token_type    | varchar(40)  | YES  |     | NULL    |                |
| access_token  | varchar(255) | YES  | UNI | NULL    |                |
| refresh_token | varchar(255) | YES  | UNI | NULL    |                |
| expires       | datetime     | YES  |     | NULL    |                |
| _scopes       | text         | YES  |     | NULL    |                |
| added_at      | datetime     | YES  |     | NULL    |                |
+---------------+--------------+------+-----+---------+----------------+
"""


class OauthAccessTokenEntity(db.Model, CRUDMixin):
    """
    Access tokens are used for accessing protected data.
    """
    __tablename__ = 'oauth_access_token'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.String(40), db.ForeignKey(OauthClientEntity.client_id),
        nullable=False
    )
    client = db.relationship(OauthClientEntity, uselist=False, lazy='joined')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))
    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)

    # Note: this column stores UTC values
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)
    added_at = db.Column('added_at', db.DateTime, nullable=False)

    @property
    def user(self):
        return self.client.user if self.client else None

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    def is_expired(self):
        """
        Note: If the `expires` attribute is None we consider the token expired.

        :rtype bool: true if 'expires' datetime > the current UTC datetime

        """
        if self.expires:
            return self.expires < datetime.utcnow()
        return True

    @property
    def expires_in(self):
        """
        :rtype int: the number of seconds left until the token expiration
        """
        secs = 0

        if not self.is_expired():
            diff = self.expires - datetime.utcnow()
            secs = int(diff.total_seconds()) + 1

        return secs

    def serialize(self):
        """
        It is very important to return at least the following three values:

            - id: used for lookups
            - access_token: used in the request "Authorization" header
            - expires_in: used to determine if we need to generate a new token

        """
        return {
            'id': self.id,
            'token_type': self.token_type,
            'access_token': self.access_token,
            'expires_in': self.expires_in,
            '.expires_on_utc': utils.serialize_date_utc(self.expires),
            '.expires_on_local': utils.serialize_date_est(self.expires),
        }

    def __repr__(self):
        """ Return a friendly object representation """
        return "<OauthAccessTokenEntity(id: {0.id}, "\
            "token_type: {0.token_type}, " \
            "user_id: {0.user.id}, " \
            "expires: {0.expires}, " \
            "expires_in: {0.expires_in}, " \
            "scopes: {0.scopes}, " \
            "added_at: {0.added_at})>".format(self)
