"""
ORM for "linkage" table

@authors:
    Andrei Sura <sura.andrei@gmail.com>
"""
import binascii
from olass import utils
from olass.models.crud_mixin import CRUDMixin
from olass.models.partner_entity import PartnerEntity
from olass.main import db

"""
+------------------+---------------------+------+-----+---------+
| Field            | Type                | Null | Key | Default |
+------------------+---------------------+------+-----+---------+
| linkage_id       | bigint(20) unsigned | NO   | PRI | NULL    |
| partner_id       | int(10) unsigned    | NO   | MUL | NULL    |
| linkage_uuid     | binary(16)          | NO   | MUL | NULL    |
| linkage_hash     | binary(32)          | NO   | MUL | NULL    |
| linkage_added_at | datetime            | NO   | MUL | NULL    |
+------------------+---------------------+------+-----+---------+
"""


class LinkageEntity(db.Model, CRUDMixin):

    """ Maps the UUIDs to "hashed chunks" """
    __tablename__ = 'linkage'

    id = db.Column('linkage_id', db.Integer, primary_key=True)
    partner_id = db.Column('partner_id', db.Integer,
                           db.ForeignKey('partner.partner_id'), nullable=False)
    linkage_uuid = db.Column('linkage_uuid', db.Binary, nullable=False)
    linkage_hash = db.Column('linkage_hash', db.Binary, nullable=False)
    linkage_addded_at = db.Column('linkage_added_at', db.DateTime,
                                  nullable=False)

    # @OneToOne
    partner = db.relationship(PartnerEntity, uselist=False, lazy='joined')

    @staticmethod
    def short_hash(val):
        return val[:8]

    @staticmethod
    def load_paginated(per_page=25, page_num=1):
        """
        Helper for formating a list of linkages
        """
        def item_from_entity(entity):
            return {
                'id': entity.id,
                'partner_code': entity.partner.partner_code,
                'added_at': entity.date_time.strftime(
                    utils.FORMAT_US_DATE_TIME)
            }

        pagination = LinkageEntity.query.paginate(page_num, per_page, False)
        items = map(item_from_entity, pagination.items)
        return items, pagination.pages

    def friendly_uuid(self):
        return utils.hexlify(self.linkage_uuid)

    def friendly_hash(self):
        return utils.hexlify(self.linkage_hash)

    @staticmethod
    def get_chunks_cache(chunks):
        """
        From the list [x, y, z] of chunks return
        a dictionary like:

            {x: LinkageEntity, y: LinkageEntity, z: None}
        """
        bin_chunks = [binascii.unhexlify(chunk.encode('utf-8'))
                      for chunk in chunks]
        links = LinkageEntity.query.filter(
            LinkageEntity.linkage_hash.in_(bin_chunks)).all()
        links_cache = {link.friendly_hash(): link for link in links}

        result = {}
        for chunk in chunks:
            result[chunk] = links_cache.get(chunk, None)

        return result

    @staticmethod
    def get_distinct_uuids_for_chunks(chunks_cache):
        """
        From the list [x, y, z] of chunks return the set(uuid_1, uuid_2)
        if the database contains the following rows:
            x => uuid_1
            y => uuid_1
            z => uuid_2

        """
        result = set()

        for link in chunks_cache.values():
            if link:
                result.add(link.friendly_uuid())

        return result

    def __repr__(self):
        """ Return a friendly object representation """

        return "<LinkageEntity(linkage_id: {0.id}, "\
            "partner_id: {0.partner_id}, " \
            "linkage_uuid: {1}, "\
            "linkage_hash: {2}, "\
            "linkage_addded_at: {0.linkage_addded_at})>".format(
                self,
                binascii.hexlify(self.linkage_uuid),
                binascii.hexlify(self.linkage_hash)
            )
