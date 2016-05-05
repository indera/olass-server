"""
ORM for "partner" table

@authors:
    Andrei Sura <sura.andrei@gmail.com>
"""

# from olass import utils
from olass.models.crud_mixin import CRUDMixin
from olass.main import db

"""
+---------------------+------------------+------+-----+---------+
| Field               | Type             | Null | Key | Default |
+---------------------+------------------+------+-----+---------+
| partner_id          | int(10) unsigned | NO   | PRI | NULL    |
| partner_code        | char(5)          | NO   | UNI | NULL    |
| partner_description | varchar(255)     | NO   |     | NULL    |
| partner_added_at    | datetime         | NO   |     | NULL    |
+---------------------+------------------+------+-----+---------+
"""

class PartnerEntity(db.Model, CRUDMixin):

    """ Store partners sendig us the data """
    __tablename__ = 'partner'

    id = db.Column('partner_id', db.Integer, primary_key=True)
    partner_code = db.Column('partner_code', db.Text, nullable=False)
    partner_description = db.Column('partner_description', db.Text,
                                    nullable=False)
    partner_added_at = db.Column('partner_added_at', db.DateTime,
                                 nullable=False)

    def __repr__(self):
        """ Return a friendly object representation """
        return "<PartnerEntity(partner_id: {0.id}, "\
            "partner_code: {0.partner_code}, " \
            "partner_description: {0.partner_description}, " \
            "partner_addded_at: {0.partner_added_at})>".format(self)
