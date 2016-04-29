"""
Goal: Extend the base test class by inserting sample rows in the database

Authors:
     Andrei Sura <sura.andrei@gmail.com>
"""
# import uuid
from binascii import hexlify
from base_test import BaseTestCase
from olass import utils
from olass.main import db

# from olass.models.role_entity import ROLE_ADMIN, ROLE_SITE_ADMIN,\
# ROLE_SITE_USER
# from olass.models.role_entity import RoleEntity

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
from olass.models.partner_entity import PartnerEntity
from olass.models.rule_entity import RuleEntity
from olass.models.linkage_entity import LinkageEntity
from olass.models.person import Person

from olass.models.rule_entity import RULE_CODE_F_L_D_Z


class BaseTestCaseWithData(BaseTestCase):

    """ Add data... """

    def setUp(self):
            db.create_all()
            self.create_partners()
            self.create_rules()
            self.create_oauth_users()
            self.create_sample_data()

    def create_partners(self):
            """
            Create rows
            """
            added_date = utils.get_db_friendly_date_time()
            partner_uf = PartnerEntity.create(
                partner_code="UF",
                partner_description="University of Florida",
                partner_added_at=added_date)

            partner_fh = PartnerEntity.create(
                partner_code="FH",
                partner_description="Florida Hospital",
                partner_added_at=added_date)

            self.assertEquals(1, partner_uf.id)
            self.assertEquals(2, partner_fh.id)
            self.assertEquals("UF", partner_uf.partner_code)
            self.assertEquals("FH", partner_fh.partner_code)

            # verify that more than one
            with self.assertRaises(MultipleResultsFound):
                    PartnerEntity.query.filter(
                        PartnerEntity.
                        partner_description.like(
                            '%Florida%')).one()

    def create_rules(self):
        """
        Create rows
        """
        added_date = utils.get_db_friendly_date_time()

        with self.assertRaises(NoResultFound):
                RuleEntity.query.filter_by(id=1).one()

        rule = RuleEntity.create(
            rule_code=RULE_CODE_F_L_D_Z,
            rule_description='First Last Date Zip',
            rule_added_at=added_date)
        self.assertEquals(1, rule.id)

    def create_sample_data(self):
        """ Add some data """
        added_date = utils.get_db_friendly_date_time()

        sample_data = [
            {"first": "Aida", "last": " Xenon", "dob": "1910-11-12",
                "zip": "19116", "city": "GAINESVILLE"},
            {"first": "aida", "last": "xeNon ", "dob": "1910/11/12",
                "zip": "19116", "city": "gainesville"},
            {"first": "AIDA", "last": "XENON ", "dob": "1910:11:12  ",
                "zip": "19116", "city": "Gainesville"},
            {"first": "AiDa", "last": "XEnON ", "dob": "19101112  ",
                "zip": "19116", "city": "gainesviLLe"},
            {"first": "John", "last": "Doe", "dob": "1900-01-01",
                "zip": "32606", "city": "Palatca"},
            {"first": "JOHN", "last": "DOE", "dob": "1900-01-01",
                "zip": "32607", "city": "Palatca"}, ]

        partner = PartnerEntity.query.filter_by(
            partner_code='UF').one()
        rule = RuleEntity.query.filter_by(
            rule_code=RULE_CODE_F_L_D_Z).one()

        for person_data in sample_data:
            person_orig = Person(person_data)
            person = Person.get_prepared_person(person_data)
            pers_uuid = utils.get_uuid_hex()
            hashes = utils.get_person_hash(person, [rule])

            for rule_id, ahash in hashes.items():
                link = LinkageEntity.create(
                    partner_id=partner.id,
                    rule_id=rule_id,
                    linkage_uuid=pers_uuid,
                    linkage_hash=ahash,
                    linkage_addded_at=added_date)
                self.assertIsNotNone(link)

                links_by_hash = LinkageEntity.query.filter_by(
                    linkage_hash=ahash).all()

                print("==> Found {} link(s) for [{}] using hash: {}".format(
                    len(links_by_hash),
                    person_orig,
                    hexlify(ahash)))

    def create_oauth_users(self):
        """ Add user, role, user_role
        Note: partners should exist
        """
        pass
