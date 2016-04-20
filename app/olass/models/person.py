"""
Goal: store attributes for a person object

Authors:
    Andrei Sura <sura.andrei@gmail.com>

"""
from olass import utils

class Person(object):

    def __init__(self, data):
        """
        set the class attributes from the `data` dictionary
        """
        self.first = data.get('first', None)
        self.last = data.get('last', None)
        self.dob = data.get('dob', None)
        self.zip = data.get('zip', None)
        self.city = data.get('city', None)

    @classmethod
    def get_prepared_person(cls, person_data):
        """
        Creates a person object with every attribute prepared
        for hashing.

        .. seealso::

            :meth:`utils.prepare_for_hashing`
        """
        person = Person(person_data)
        person.first = utils.prepare_for_hashing(person.first)
        person.last = utils.prepare_for_hashing(person.last)
        person.dob = utils.prepare_for_hashing(person.dob)
        person.zip = utils.prepare_for_hashing(person.zip)
        person.city = utils.prepare_for_hashing(person.city)
        return person

    def __repr__(self):
        """ Return a friendly object representation """
        return "<Person (first: {0.first}, "\
            "last: {0.last}, "\
            "dob: {0.dob}, "\
            "zip: {0.zip}, "\
            "city: {0.city})>".format(self)
