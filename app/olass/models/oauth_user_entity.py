"""
ORM for "oauth_user"

@authors:
    Andrei Sura <sura.andrei@gmail.com>


Note: we use passlib for password hashing/verification
    https://pythonhosted.org/passlib/new_app_quickstart.html
"""

from passlib.apps import custom_app_context as pwd_context

from flask_login import UserMixin
from olass.models.crud_mixin import CRUDMixin
from olass.main import db
from olass.models.partner_entity import PartnerEntity
from olass.models.oauth_role_entity import OauthRoleEntity
from olass.models.oauth_user_role_entity import OauthUserRoleEntity


"""
+---------------+--------------+------+-----+---------+----------------+
| Field         | Type         | Null | Key | Default | Extra          |
+---------------+--------------+------+-----+---------+----------------+
| id            | int(11)      | NO   | PRI | NULL    | auto_increment |
| email         | varchar(255) | NO   | UNI | NULL    |                |
| first_name    | varchar(255) | YES  |     | NULL    |                |
| last_name     | varchar(255) | YES  |     | NULL    |                |
| mi_name       | char(1)      | YES  |     | NULL    |                |
| password_hash | varchar(255) | YES  |     | NULL    |                |
| added_at      | datetime     | YES  |     | NULL    |                |
+---------------+--------------+------+-----+---------+----------------+
"""


class OauthUserEntity(db.Model, UserMixin, CRUDMixin):
    """
    A user, or resource owner, is usually the registered user on your site.
    """
    __tablename__ = 'oauth_user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    mi_name = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    added_at = db.Column('added_at', db.DateTime, nullable=False)

    # Indirect mappings via `oauth_user_role` table
    partner = db.relationship(
        PartnerEntity,
        secondary=OauthUserRoleEntity.__tablename__,
        primaryjoin="oauth_user.c.id==oauth_user_role.c.user_id",
        secondaryjoin="oauth_user_role.c.partner_id==partner.c.partner_id",
        backref=db.backref('oauth_user'),
        uselist=False,
    )

    role = db.relationship(
        OauthRoleEntity,
        secondary=OauthUserRoleEntity.__tablename__,
        primaryjoin="oauth_user.c.id==oauth_user_role.c.user_id",
        secondaryjoin="oauth_user_role.c.role_id==oauth_role.c.id",
        backref=db.backref('oauth_user'),
        uselist=False,
    )

    def hash_password(self, password):
        """
        @see
            https://www.akkadia.org/drepper/SHA-crypt.txt
        """
        self.password_hash = pwd_context.encrypt(password,
                                                 scheme='sha512_crypt',
                                                 category='admin')

    def verify_password(self, password):
        """ Return true if password matches the stored hash """
        return pwd_context.verify(password, self.password_hash,
                                  scheme='sha512_crypt')
    # scheme='bcrypt')
    # scheme='bcrypt_sha256')
    # scheme='pbkdf2_sha512')

    # def is_authenticated(self):
    #     """ Returns True if the user is authenticated, i.e. they have provided
    #     valid credentials.
    #     """
    #     return True

    # def is_anonymous(self):
    #     """ Flag instances of valid users """
    #     return False

    def serialize(self):
        """ Helper for sending data in http responses """
        return {
            'id': self.id,
            'email': self.email,
            'added_at': self.added_at.isoformat(),
        }

    def __repr__(self):
        """ Return a friendly object representation """
        display_partner = self.partner.partner_code if self.partner else ''
        display_role = self.role.role_code if self.role else ''

        return "<UserEntity(id: {0.id}, "\
            "email: {0.email}, " \
            "partner_code: {1}, " \
            "role_code: {2}, " \
            "added_at: {0.added_at})>".format(
                self, display_partner, display_role)
