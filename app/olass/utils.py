"""
Goal: Store helper functions not tied to a specific module

@authors:
    Andrei Sura <sura.andrei@gmail.com>
"""

import uuid
import sys
import unicodedata
import functools
# import hmac
# import base64
# import pytz as tz

# from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
from flask import flash
from flask import jsonify
# from hashlib import sha512
from binascii import unhexlify


FORMAT_US_DATE = "%x"
FORMAT_US_DATE_TIME = '%x %X'
FORMAT_US_DATE_TIME_ZONE = '%x %X %Z%z'
FORMAT_DATABASE_DATE_TIME = "%Y-%m-%d %H:%M:%S"

FLASH_CATEGORY_ERROR = 'error'
FLASH_CATEGORY_INFO = 'info'

UNICODE_ASCII_CHARACTER_SET = ('abcdefghijklmnopqrstuvwxyz'
                               'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                               '0123456789')


# table of punctuation characters + space
tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                    if unicodedata.category(chr(i)).startswith('P') or
                    chr(i) in [' '])


# def generate_token_urandom(length=40):
#     """Generates a non-guessable OAuth token
#
#     OAuth 2.0 rfc does not specify the format of tokens except that they
#     should be strings of random characters.
#     """
#     from base64 import b64encode
#     from os import urandom
#     return b64encode(urandom(length))


def generate_token(length=40, chars=UNICODE_ASCII_CHARACTER_SET):
    """Generates a non-guessable OAuth token

    OAuth 2.0 rfc does not specify the format of tokens except that they
    should be strings of random characters.
    """
    from random import SystemRandom
    rand = SystemRandom()
    return ''.join(rand.choice(chars) for x in range(length))


def prepare_for_hashing(text):
    return text.translate(tbl).lower()


def get_uuid_hex(uuid_text=None):
    if not uuid_text:
        uuid_text = uuid.uuid1()
    return unhexlify(str(uuid_text).replace('-', '').lower().encode())


def replace_all(text, replacements):
    """
    Replace in `text` all strings specified in `replacements`
    Example: replacements = ('hello', 'goodbye'), ('world', 'earth')
    """
    return functools.reduce(lambda a, kv: a.replace(*kv), replacements, text)


# def clean_str(dangerous):
#     """ Return the trimmed string """
#     if dangerous is None:
#         return None
#     return str(dangerous).strip()
#
#
# def clean_int(dangerous):
#     """
#     Return None for non-integer input
#     """
#     if dangerous is None:
#         return None
#
#     dangerous = str(dangerous).strip()
#
#     if "" == dangerous:
#         return None
#
#     if not dangerous.isdigit():
#         return None
#
#     return int(dangerous)
#
#
# def get_safe_int(unsafe, default=1, min_allowed=1, max_allowed=None):
#     """ Helper method for reading the user input
#
#     :param unsafe: the user input to be interpreted as in
#     :param default: the default to use if unable to convert the int
#     :param min_allowed: the minimum value to use
#     :param max_allowed: the maximum value to use (ignores None value)
#     """
#     unsafe = clean_int(unsafe)
#     if unsafe is None:
#         unsafe = default
#     elif unsafe < min_allowed:
#         unsafe = min_allowed
#     elif max_allowed is not None and unsafe > max_allowed:
#         unsafe = max_allowed
#     return unsafe


def flash_error(msg):
    """ Put a message in the "error" queue for display """
    flash(msg, FLASH_CATEGORY_ERROR)


def flash_info(msg):
    """ Put a message in the "info" queue for display """
    flash(msg, FLASH_CATEGORY_INFO)


def jsonify_error(data):
    """ Format an error message to be json-friendly """
    return jsonify({'status': 'error', 'data': data})


def jsonify_success(data):
    """ Format a success message to be json-friendly """
    return jsonify({'status': 'success', 'data': data})


def get_expiration_date(offset_days):
    """
    :param offset_days: how many days to shift versus today
    :rtype datetime
    :return the date computed with offset_days
    """
    return datetime.now() + timedelta(days=offset_days)


def get_db_friendly_date_time_string():
    """
    :rtype: string
    :return current time in format: "YYYY-MM-DD 01:23:45"
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_db_friendly_date_time(when=None):
    """
    :rtype: date
    :return current time in format: "YYYY-MM-DD 01:23:45"
    """
    if not when:
        when = datetime.now()
    return when.replace(microsecond=0)


# def localize_datetime(value, zone_name='US/Eastern'):
#     """ Localize the specified datetime value according to a zone"""
#     # print(tz.all_timezones)
#     if value is None:
#         return ''
#     timezone = tz.timezone(zone_name)
#     localized_value = timezone.localize(value, is_dst=None)
#     return localized_value
#
#
# def localize_est_date(value):
#     """ Format the datetime value as `FORMAT_US_DATE` """
#     localized_value = localize_datetime(value)
#     return localized_value.strftime(FORMAT_US_DATE)
#
#
# def localize_est_datetime(value):
#     """ Format the datetime value as `FORMAT_US_DATE_TIME` """
#     localized_value = localize_datetime(value)
#     if value is None or '' == value:
#         return ''
#     return localized_value.strftime(FORMAT_US_DATE_TIME)


# def get_email_token(email, salt, secret):
#     """
#     Generate a timestamped token from the specified email
#     """
#     ts = URLSafeTimedSerializer(secret)
#     token = ts.dumps(email, salt=salt)
#     return token
#
#
# def get_email_from_token(token, salt, secret, max_age=86400):
#     """
#     Read an email from a timestamped token.
#     Raises an exception if the token is more than 24 hours old or invalid
#     """
#     ts = URLSafeTimedSerializer(secret)
#     email = ts.loads(token, salt=salt, max_age=max_age)
#     return email
