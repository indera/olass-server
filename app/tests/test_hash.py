from passlib.hash import sha256_crypt
from passlib.hash import sha512_crypt

from base_test import BaseTestCase

"""
@see SO thread: hashlib-vs-crypt-crypt-in-python-why-different-results
"""


class TestHash(BaseTestCase):

    def test_hash(self):
        salt = 'qwerty'
        password = "password"

        value_sha256 = sha256_crypt.encrypt(password, salt=salt, rounds=5000)
        value_sha512 = sha512_crypt.encrypt(password, salt=salt, rounds=5000)

        self.assertEqual(value_sha256,
                         '$5$qwerty$LsogXlvrRvdIKby1vMIPLn3PxErB6CooS9lzWeiFfD4')
        self.assertEqual(value_sha512,
                         '$6$qwerty$yKc2cc4EDSNgZNqg.gSoVLcCI5QWuf4xCW8V0VdOVzFHHtSw.fsytKQl2g.WUIjDwJVdGD1Tw8g0Y6WAfnR1O1')
        # print("\n sha256_crypt.encryp: {}".format(value_sha256))
        # print("\n sha512_crypt.encryp: {}".format(value_sha512))

        # MacOS uses DES-based crypt and it does not match the sha512_crypt
        # import crypt
        # 6 corresponds to sha512 (see man crypt)
        # insalt = '$6${}$'.format(salt)
        # value_crypt = crypt.crypt(password, insalt)
        # print(" crypt.crypt: {}".format(value_crypt))
