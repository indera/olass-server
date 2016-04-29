"""
ORM for "oauth_user_role"

@authors:
    Andrei Sura <sura.andrei@gmail.com>
"""

from olass.models.crud_mixin import CRUDMixin
from olass.main import db
# from olass.models.partner_entity import PartnerEntity
# from olass.models.oauth_role_entity import OauthRoleEntity
# from olass.models.oauth_user_entity import OauthUserEntity


"""
+------------+----------------------+------+-----+---------+----------------+
| Field      | Type                 | Null | Key | Default | Extra          |
+------------+----------------------+------+-----+---------+----------------+
| id         | int(11)              | NO   | PRI | NULL    | auto_increment |
| partner_id | int(10) unsigned     | NO   | MUL | NULL    |                |
| user_id    | int(11)              | NO   | UNI | NULL    |                |
| role_id    | smallint(5) unsigned | NO   | MUL | NULL    |                |
| added_at   | datetime             | YES  |     | NULL    |                |
+------------+----------------------+------+-----+---------+----------------+
"""


class OauthUserRoleEntity(db.Model, CRUDMixin):

    """ Map users to a role and partner """
    __tablename__ = 'oauth_user_role'

    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(
        db.Integer, db.ForeignKey('partner.partner_id'), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey('oauth_user.id'), nullable=False)
    role_id = db.Column(
        db.Integer, db.ForeignKey('partner.partner_id'), nullable=False)
    added_at = db.Column(db.DateTime, nullable=False)

    # @OneToOne
    # partner = db.relationship(PartnerEntity, uselist=False, lazy='joined')
    # user = db.relationship(OauthUserEntity, uselist=False, lazy='joined')
    # role = db.relationship(OauthRoleEntity, uselist=False, lazy='joined')

    def __repr__(self):
        return "<UserRole(id: {0.id}, " \
            "partner_id: {0.partner_id}, " \
            "user_id: {0.user_id}, " \
            "role_id: {0.role_id}, " \
            "added_at: {0.added_at})>".format(self)
