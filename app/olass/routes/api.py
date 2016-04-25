"""
Goal: Delegate requests to the `/api` path to the appropriate controller

@authors:
    Andrei Sura <sura.andrei@gmail.com>
"""
from binascii import unhexlify
import collections
# from datetime import datetime
from flask import request
# from flask import session
# from flask import make_response
# from flask_login import login_required

from olass import utils
from olass.main import app
from olass.models.linkage_entity import LinkageEntity


@app.route('/api/', methods=['POST', 'GET'])
# @login_required
def api_hello():
    """ Say hello """
    return utils.jsonify_success({
        'message': 'Hello'
    })


@app.route('/api/check', methods=['POST', 'GET'])
def api_check_existing():
    """
    For each chunk verify if it exists in the database.

    == Example input json:

{
  "partner": "hcn",
  "data":
        {
        "1": ["abc...", "def..."],
        "2": ["xyz...", "123..."],
        }
}

    == Example of output json:

{
  "data": {
    "1": {
      "abc...": {
        "is_found": 1,
        "rule": "F_L_D_Z"
      },
      "def...": {
        "is_found": 1,
        "rule": "L_F_D_Z"
      }
    },
    "2": {
     "xyz...": ...
     "123...": ...

    """
    json = request.get_json(silent=False)
    if not json:
        err = "Invalid json object specified"
        app.logger.error(err)
        return utils.jsonify_error(err)

    app.logger.info("call api_check_existing() from partner: {}"
                    .format(json['partner']))

    result = collections.defaultdict(dict)

    # init the response dictionary
    for pat_id, pat_chunks in json['data'].items():
        short_chunks = [LinkageEntity.short_hash(x) for x in pat_chunks]
        result[pat_id] = dict.fromkeys(short_chunks)

    # patient chunks are received in groups
    for pat_id, pat_chunks in json['data'].items():
        app.logger.debug("Working on chunks for patient [{}]".format(pat_id))

        for chunk in pat_chunks:
            if len(chunk) != 64:
                app.logger.warn("Skip chunk for patient [{}] with length: {}"
                                .format(pat_id, len(chunk)))
                continue

            app.logger.info("check chunk: {}".format(chunk))
            binary_hash = unhexlify(chunk)
            link = LinkageEntity.query.filter_by(
                linkage_hash=binary_hash).one_or_none()

            short_chunk = LinkageEntity.short_hash(chunk)

            if link:
                result[pat_id][short_chunk] = \
                    {"is_found": 1, "rule": link.rule.rule_code}
            else:
                result[pat_id][short_chunk] = {"is_found": 0}

    return utils.jsonify_success(result)
