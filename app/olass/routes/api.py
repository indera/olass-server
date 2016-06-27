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
from olass.models.linkage_entity import LinkageEntity
from olass.models.oauth_access_token_entity import OauthAccessTokenEntity

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


def get_partner_from_token(access_token):
    """
    Walk the token->client->user->partner chain so we can
    connect the the `LinkageEntity` row to a `PartnerEntity`
    """
    tok = OauthAccessTokenEntity.query.filter_by(
        access_token=access_token).one_or_none()
    log.debug("get_partner_from_token found: {}".format(tok))
    return tok.client.user.partner


@app.route('/api/save', methods=['POST', 'GET'])
@auth.require_oauth()
def api_save_patient_hashes():
    """
    For each chunk save a new uuid or return an existing one from the database.

== Example of input json:
{
"data": {
   "1": {
       "1": "b2cdaea3d7c9891b2ed94d1973fe5085183e4bb4bd87b672e066a456ee67bd38"
       },

   "2": {
       "1": "345b192ae4093dcbc5c914bdcb5e8c41e58162475a295c88b1ce594bd3dd78f7",
       "2": "1dcce10470c0ea73a8a6287f69f4f862c5e13faea7c11104fae07dbc8d5ce56e"
       },
   "3": {
       "1": "995b192ae4093dcbc5c914bdcb5e8c41e58162475a295c88b1ce594bd3dd78f7"
       }
   }
}

== To find the rows in the database:
select hex(linkage_uuid), hex(linkage_hash) from linkage order by linkage_id;

    """
    auth_pieces = request.headers.get('Authorization').split(' ')
    log.debug("Authorization_header: {}".format(auth_pieces))
    access_token = auth_pieces[1].strip()
    partner = get_partner_from_token(access_token)
    json = request.get_json(silent=False)

    if not json:
        err = "Invalid json object specified"
        log.error(err)
        return utils.jsonify_error(err)

    result = collections.defaultdict(dict)
    json_data = json['data']

    # patient chunks are received in groups
    for pat_id, pat_chunks in json_data.items():
        # Since there is a chance of duplicate chunks find uniques
        chunks = list(set(chunk for chunk_num, chunk in pat_chunks.items()))
        chunks_cache = LinkageEntity.get_chunks_cache(chunks)
        uuids = LinkageEntity.get_distinct_uuids_for_chunks(chunks_cache)
        log.debug("Found [{}] matching uuids from [{}] chunks of patient "
                  "[{}]".format(len(uuids), len(chunks), pat_id))

        added_date = utils.get_db_friendly_date_time()

        if len(uuids) == 0:
            binary_uuid = utils.get_uuid_bin()
            hex_uuid = utils.hexlify(binary_uuid)
            log.debug("Generate [{}] for pat_id[{}]".format(pat_id, hex_uuid))
        elif len(uuids) >= 1:
            hex_uuid = uuids.pop()
            binary_uuid = unhexlify(hex_uuid.encode('utf-8'))

            # after pop() the list with one item is empty
            if not uuids:
                log.debug("Reuse [{}] for pat_id[{}]".format(pat_id, hex_uuid))
            else:
                log.warning("More than one uuid for chunks attributed to "
                            "[{}] patient [{}]"
                            .format(partner.partner_code, pat_id))
                log.warning("\n==>chunks: {}\n==> uuids: {}"
                            .format(chunks, uuids))
        # update the response json
        result[pat_id] = {"uuid": hex_uuid}

        for i, chunk in enumerate(chunks):
            if chunks_cache.get(chunk):
                log.debug("Skip chunk [{}] - already linked".format(chunk))
                continue

            # link every chunk to the same uuid
            binary_hash = unhexlify(chunk.encode('utf-8'))
            LinkageEntity.create(
                partner_id=partner.id,
                linkage_uuid=binary_uuid,
                linkage_hash=binary_hash,
                linkage_added_at=added_date)
            log.debug("Created link [{}] for [{}]".format(i, chunk))

    return utils.jsonify_success(result)
