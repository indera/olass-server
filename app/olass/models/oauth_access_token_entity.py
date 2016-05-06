"""
ORM for 'oauth_access_token' table

"""
from olass.models.crud_mixin import CRUDMixin
from olass.models.oauth_client_entity import OauthClientEntity
from olass.main import db

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
        db.String(40), db.ForeignKey(OauthClientEntity.id),
        nullable=False
    )
    client = db.relationship(OauthClientEntity, uselist=False, lazy='joined')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))
    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)
    added_at = db.Column('added_at', db.DateTime, nullable=False)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    def __repr__(self):
        """ Return a friendly object representation """
        return "<OauthAccessTokenEntity(id: {0.id}, "\
            "token_type: {0.token_type}, " \
            "client_id: {0.client_id}, " \
            "access_token: {0.access_token}, " \
            "refresh_token: {0.refresh_token}, " \
            "expires: {0.expires}, " \
            "added_at: {0.added_at})>".format(self)
