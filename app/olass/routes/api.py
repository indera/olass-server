"""
Goal: Delegate requests to the `/api` path to the appropriate controller

@authors:
    Andrei Sura <sura.andrei@gmail.com>
"""
import collections
from binascii import unhexlify
from flask import request
from flask_login import login_required
from flask_login import current_user

from olass import utils
from olass.main import app
from olass.models.partner_entity import PartnerEntity
from olass.models.linkage_entity import LinkageEntity

from .oauth import oauth as auth
log = app.logger


@app.route('/api/', methods=['POST', 'GET'])
@app.route('/api/hello', methods=['POST', 'GET'])
@login_required
def say_hello():
    """ Say hello """
    return utils.jsonify_success({
        'message': 'Hello {}! You are logged in.'.format(current_user.email)
    })


@app.route('/api/me', methods=['POST', 'GET'])
@auth.require_oauth()
def me():
    user = request.oauth.user
    return utils.jsonify_success({
        'user': user.serialize(),
        'client': request.oauth.client.serialize()
    })


@app.route('/api/save', methods=['POST', 'GET'])
@auth.require_oauth()
def api_save_patient_hashes():
    """
    For each chunk save a new uuid or return an existing one from the database.

== Example of input json:
{
  "partner_code": "UF",
  "data": {
"1":
   [{"chunk_num": "1",
   "chunk": "8b31efa965d46f971426ac9c133db1c769a712657b74410016d636b10a996506"}
   ],
"2":
   [{"chunk_num": "1",
   "chunk": "db07840bf253e5e6c16cabaca97fcc4363643f8552d65ec04290f3736d72b27d"},
   {"chunk_num": "2",
   "chunk": "c79db51a3f0037ef83f45b4a85bc519665dbf9de8adf9f47d4a73a0c5bb91caa"}
   ]
}
}

== Example of output json:
{
    "data": {
        "1": {
            "uuid": "ebd9ae1a1ba011e694c84d46767d11db"
        },
        "2": {
            "uuid": "ebd9b9d21ba011e694c84d46767d11db"
        }
    },
    "status": "success"
}

== Rows in db
select hex(linkage_uuid), hex(linkage_hash) from linkage order by linkage_id;
+----------------------------------+------------------
| hex(linkage_uuid)                | hex(linkage_hash)
+----------------------------------+------------------
| ebd9ae1a1ba011e694c84d46767d11db | 8b31efa965d46f971 ...
| ebd9b9d21ba011e694c84d46767d11db | db07840bf253e5e6c ...
| ebd9b9d21ba011e694c84d46767d11db | c79db51a3f0037ef8 ...
+----------------------------------+------------------

    """
    log.debug('request.headers: {}'.format(request.headers))
    json = request.get_json(silent=False)

    if not json:
        err = "Invalid json object specified"
        log.error(err)
        return utils.jsonify_error(err)

    # log.debug("call api_save_patient_hashes() "
    #           "from partner_code [{}] for [{}] patients"
    #           .format(json['partner_code'], len(json['data'].keys())))

    result = collections.defaultdict(dict)

    # init the response dictionary
    for pat_id, pat_chunks in json['data'].items():
        chunks = [x.get('chunk') for x in pat_chunks]
        result[pat_id] = dict.fromkeys(chunks)

    # @TODO: move input validation to a dedicated function
    # find the proper partner id
    partner_code = json['partner_code']

    if not (1 <= len(partner_code) <= 5):
        raise Exception("Invalid partner code length: {}"
                        .format(len(partner_code)))
    partner = PartnerEntity.query.filter_by(
        partner_code=partner_code).one_or_none()

    if not partner:
        raise Exception("Invalid partner code: {}".format(partner_code))

    # patient chunks are received in groups
    for pat_id, pat_chunks in json['data'].items():
        chunks = [x.get('chunk') for x in pat_chunks]
        chunks_cache = LinkageEntity.get_chunks_cache(chunks)
        uuids = LinkageEntity.get_distinct_uuids_for_chunks(chunks_cache)
        # log.debug("Found [{}] matching uuids from [{}] chunks of patient "
        #          "[{}]".format(len(uuids), len(chunks), pat_id))

        if len(uuids) == 0:
            # log.debug("generate new uuid for pat_id [{}]".format(pat_id))
            binary_uuid = utils.get_uuid_hex()

            link = None

            for chunk_data in pat_chunks:
                # link every chunk to the same uuid
                added_date = utils.get_db_friendly_date_time()
                chunk = chunk_data['chunk']
                chunk_num = chunk_data['chunk_num']
                binary_hash = unhexlify(chunk.encode('utf-8'))

                link = LinkageEntity.create(
                    partner_id=partner.id,
                    linkage_uuid=binary_uuid,
                    linkage_hash=binary_hash,
                    linkage_addded_at=added_date)
                log.debug("Created link for chunk_num: {}".format(chunk_num))
            # update the response json
            result[pat_id] = {"uuid": link.friendly_uuid()}

        elif len(uuids) == 1:
            uuid = uuids.pop()
            # log.debug("Reusing the uuid [{}]".format(uuid))

            link = None

            for chunk_data in pat_chunks:
                # link every chunk to the same uuid
                chunk = chunk_data['chunk']
                binary_hash = unhexlify(chunk.encode('utf-8'))
                binary_uuid = unhexlify(uuid.encode('utf-8'))
                link = chunks_cache.get(chunk)

                if not link:
                    log.info("Attempt to insert for hash [{}]".format(chunk))
                    added_date = utils.get_db_friendly_date_time()
                    link = LinkageEntity.create(
                        partner_id=partner.id,
                        linkage_uuid=binary_uuid,
                        linkage_hash=binary_hash,
                        linkage_addded_at=added_date)
            result[pat_id] = {"uuid": link.friendly_uuid()}

        else:
            log.error("It looks like we got a collision for chunks: {}"
                      .format(chunks, uuids))
            raise Exception("More than one uuid for chunks attributed to"
                            "[{}] patient [{}]".format(partner_code, pat_id))

        for chunk_data in pat_chunks:
            chunk = chunk_data['chunk']

            # validate the input
            if len(chunk) != 64:
                log.warning("Skip chunk for patient [{}] with length: {}"
                            .format(pat_id, len(chunk)))
                continue

    return utils.jsonify_success(result)
