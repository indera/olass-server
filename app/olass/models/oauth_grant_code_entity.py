"""
ORM for 'oauth_grant_code' table

"""
from olass.models.crud_mixin import CRUDMixin
from olass.models.oauth_client_entity import OauthClientEntity
from olass.main import db

"""
+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| id           | int(11)      | NO   | PRI | NULL    | auto_increment |
| client_id    | varchar(40)  | NO   | MUL | NULL    |                |
| code         | varchar(255) | NO   | MUL | NULL    |                |
| redirect_uri | varchar(255) | YES  |     | NULL    |                |
| expires      | datetime     | YES  |     | NULL    |                |
| _scopes      | text         | YES  |     | NULL    |                |
| added_at     | datetime     | YES  |     | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+
"""

class OauthGrantCodeEntity(db.Model, CRUDMixin):
    """
    A grant code is created in the authorization flow, and will be destroyed
    when the authorization finished.
    @TODO: implement using redis
    """
    __table_name__ = 'oauth_grant_code'

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(
        # db.String(40), db.ForeignKey('oauth_client.id'),
        db.String(40), db.ForeignKey(OauthClientEntity.id),
        nullable=False
    )
    client = db.relationship(OauthClientEntity, uselist=False, lazy='joined')

    code = db.Column(db.String(255), index=True, nullable=False)
    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)
    added_at = db.Column('added_at', db.DateTime, nullable=False)

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()
    #     return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    def __repr__(self):
        """ Return a friendly object representation """
        return "<OauthGrantCodeEntity(id: {0.id}, "\
            "client_id: {0.client_id}, " \
            "code: {0.code}, " \
            "expires: {0.expires}, " \
            "added_at: {0.added_at})>".format(self)
