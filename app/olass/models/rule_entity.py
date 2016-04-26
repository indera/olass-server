"""
ORM for "rule" table

@authors:
    Andrei Sura <sura.andrei@gmail.com>

+------------------+------------------+------+-----+---------+
| Field            | Type             | Null | Key | Default |
+------------------+------------------+------+-----+---------+
| rule_id          | int(10) unsigned | NO   | PRI | NULL    |
| rule_code        | varchar(255)     | NO   | UNI | NULL    |
| rule_description | varchar(255)     | NO   |     | NULL    |
| rule_added_at    | datetime         | NO   |     | NULL    |
+------------------+------------------+------+-----+---------+
"""

# from olass import utils
from olass.models.crud_mixin import CRUDMixin
from olass.main import db

# _1 First Name + Last Name + DOB + Zip
RULE_CODE_F_L_D_Z = 'F_L_D_Z'

# _2 Last Name + First Name + DOB + Zip
RULE_CODE_L_F_D_Z = 'L_F_D_Z'

# _3 First Name + Last Name + DOB + City
RULE_CODE_F_L_D_C = 'F_L_D_C'

# _4 Last Name + First Name + DOB + City
RULE_CODE_L_F_D_C = 'L_F_D_C'

# _5 Three Letter FN + Three Letter LN + Soundex FN + Soundex LN + DOB
RULE_CODE_3F_3L_SF_SL_D = '3F_3L_SF_SL_D'


class RuleEntity(db.Model, CRUDMixin):

    """ Store rules used by the partners sending us the data """
    __tablename__ = 'rule'

    id = db.Column('rule_id', db.Integer, primary_key=True)
    rule_code = db.Column('rule_code', db.Text, nullable=False)
    rule_description = db.Column('rule_description', db.Text,
                                 nullable=False)
    rule_added_at = db.Column('rule_added_at', db.DateTime,
                              nullable=False)

    @staticmethod
    def get_rules_cache():
        rules = RuleEntity.query.all()
        result = {rule.rule_code: rule.id for rule in rules}
        return result

    def __repr__(self):
        """ Return a friendly object representation """
        return "<RuleEntity(rule_id: {0.id}, "\
            "rule_code: {0.rule_code}, " \
            "rule_description: {0.rule_description}, " \
            "rule_addded_at: {0.rule_addded_at})>".format(self)
