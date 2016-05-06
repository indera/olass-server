"""
ORM for oauth_client table

"""
from olass.models.crud_mixin import CRUDMixin
from olass.models.oauth_user_entity import OauthUserEntity
from olass.main import db

"""
+-----------------+-------------+------+-----+---------+-------+
| Field           | Type        | Null | Key | Default | Extra |
+-----------------+-------------+------+-----+---------+-------+
| id              | varchar(40) | NO   | PRI | NULL    |       |
| client_secret   | varchar(55) | NO   |     | NULL    |       |
| user_id         | int(11)     | NO   | MUL | NULL    |       |
| _redirect_uris  | text        | YES  |     | NULL    |       |
| _default_scopes | text        | YES  |     | NULL    |       |
| added_at        | datetime    | YES  |     | NULL    |       |
+-----------------+-------------+------+-----+---------+-------+
"""

class OauthClientEntity(db.Model, CRUDMixin):
    """
    A client is the app which want to use the resource of a user. It is
    suggested that the client is registered by a user on your site, but it is
    not required.
    """
    __tablename__ = 'oauth_client'

    id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), nullable=False)

    user_id = db.Column(db.ForeignKey('oauth_user.id'))
    user = db.relationship(OauthUserEntity, uselist=False, lazy='joined')

    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)
    added_at = db.Column('added_at', db.DateTime, nullable=False)

    @property
    def client_type(self):
        """
         confidential - an application that is capable of keeping a client
         password confidential to the world. This client password is assigned
         to the client app by the authorization server. This password is used
         to identify the client to the authorization server, to avoid fraud. An
         example of a confidential client could be a web app, where no one but
         the administrator can get access to the server, and see the client
         password.

         public - an application that is not capable of keeping a client
         password confidential. For instance, a mobile phone application or a
         desktop application that has the client password embedded inside it.
         Such an application could get cracked, and this could reveal the
         password. The same is true for a JavaScript application running in the
         users browser. The user could use a JavaScript debugger to look into
         the application, and see the client password
         """
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []

    def __repr__(self):
        """ Return a friendly object representation """
        return "<OauthClientEntity(id: {0.id}, "\
            "client_secret: {0.client_secret}, " \
            "user_id: {0.user_id}, " \
            "added_at: {0.added_at})>".format(self)
