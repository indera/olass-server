"""
ORM for "oauth_role"

@authors:
    Andrei Sura <sura.andrei@gmail.com>

"""
from olass.models.crud_mixin import CRUDMixin
from olass.main import db

"""
+------------------+----------------------+------+-----+---------+
| Field            | Type                 | Null | Key | Default |
+------------------+----------------------+------+-----+---------+
| id               | smallint(5) unsigned | NO   | PRI | NULL    |
| role_code        | varchar(20)          | NO   | UNI | NULL    |
| role_description | varchar(255)         | NO   |     | NULL    |
+------------------+----------------------+------+-----+---------+
"""

class OauthRoleEntity(db.Model, CRUDMixin):
    """
    Roles so far: root, admin, staff
    """
    __tablename__ = 'oauth_role'

    id = db.Column(db.Integer, primary_key=True)
    role_code = db.Column('role_code', db.Text, nullable=False)
    role_description = db.Column('role_description', db.Text, nullable=False)
    added_at = db.Column('added_at', db.DateTime, nullable=False)

    def __repr__(self):
        return "<OauthRoleEntity(id: {0.id}, " \
            "role_code: {0.role_code}, " \
            "role_description: {0.role_description}, " \
            "added_at: {0.added_at})>".format(self)
