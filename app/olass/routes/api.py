"""
Goal: Delegate requests to the `/api` path to the appropriate controller

@authors:
    Andrei Sura <sura.andrei@gmail.com>
"""
from binascii import unhexlify
# import collections
# from datetime import datetime
from flask import request
# from flask import session
# from flask import make_response
# from flask_login import login_required

from olass import utils
from olass.main import app
from olass.models.linkage_entity import LinkageEntity

@app.route('/api/hello', methods=['POST', 'GET'])
# @login_required
def api_hello():
    """
    Say hello
    """
    return utils.jsonify_success({
        'message': 'Hello'
    })


@app.route('/api/check', methods=['POST', 'GET'])
def api_check_existing():
    """
    For each chunk verify if it exists in the database.
    """
    json = request.get_json(silent=False)
    app.logger.info("call api_check_existing() from partner: {}"
                    .format(json['partner']))

    result = {}

    for chunk in json['data']:
        if len(chunk) != 64:
            app.logger.warn("Skip chunk with length: {}".format(len(chunk)))
            continue

        app.logger.info("check chunk: {}".format(chunk))
        binary_hash = unhexlify(chunk)
        link = LinkageEntity.query.filter_by(
            linkage_hash=binary_hash).one_or_none()

        if link:
            result[chunk] = {"is_found": 1, "rule": link.rule.rule_code}
        else:
            result[chunk] = {"is_found": 0}

    return utils.jsonify_success(result)
