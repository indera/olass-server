"""
ORM for tables used for OAuth2 provider implementation

@see: https://github.com/lepture/example-oauth2-server

"""
from olass.main import db
from olass.models.crud_mixin import CRUDMixin


class User(db.Model, CRUDMixin):
    """
    A user, or resource owner, is usually the registered user on your site.
    """
    # TODO: add password column to allow web-based logins
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    addded_at = db.Column('added_at', db.DateTime, nullable=False)


class Client(db.Model, CRUDMixin):
    """
    A client is the app which want to use the resource of a user. It is
    suggested that the client is registered by a user on your site, but it is
    not required.
    """
    id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), nullable=False)

    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship(User, uselist=False, lazy='joined')

    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    @property
    def client_type(self):
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


class Grant(db.Model, CRUDMixin):
    """
    A grant token is created in the authorization flow, and will be destroyed
    when the authorization finished. In this case, it would be better to store
    the data in a cache, which would benefit a better performance.
    """
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )
    user = db.relationship(User, uselist=False, lazy='joined')

    client_id = db.Column(
        db.String(40), db.ForeignKey('client.id'),
        nullable=False
    )
    client = db.relationship(Client, uselist=False, lazy='joined')

    code = db.Column(db.String(255), index=True, nullable=False)
    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.String(40), db.ForeignKey('client.id'),
        nullable=False
    )
    client = db.relationship(Client, uselist=False, lazy='joined')

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'),
        nullable=False
    )
    user = db.relationship(User, uselist=False, lazy='joined')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
