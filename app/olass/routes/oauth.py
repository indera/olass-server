"""
Goal: Implement routes specific to OAuth2 provider

@authors:
    Andrei Sura <sura.andrei@gmail.com>

Client Credentials Grant: http://tools.ietf.org/html/rfc6749#section-4.4

Note: client credentials grant type MUST only be used by confidential clients.

--- Confidential Clients ---
Clients capable of maintaining the confidentiality of their
credentials (e.g., client implemented on a secure server with
restricted access to the client credentials), or capable of secure
client authentication using other means.

+---------+                                  +---------------+
|         |                                  |               |
|         |>--(A)- Client Authentication --->| Authorization |
| Client  |                                  |     Server    |
|         |<--(B)---- Access Token ---------<|               |
|         |                                  |               |
+---------+                                  +---------------+


                    Client Credentials Flow

The flow illustrated above includes the following steps:

(A)  The client authenticates with the authorization server and
    requests an access token from the token endpoint.

(B)  The authorization server authenticates the client, and if valid,
    issues an access token.

-------------------------------------------------------------------------------
According to the rfc6749, client authentication is required in the
following cases:

    - Resource Owner Password Credentials Grant: see `Section 4.3.2`.
    - Authorization Code Grant: see `Section 4.1.3`.
    - Refresh Token Grant: see `Section 6`.

"""
# TODO: read http://flask-oauthlib.readthedocs.io/en/latest/client.html

from datetime import datetime, timedelta
from flask_oauthlib.provider import OAuth2Provider
from flask import request
from olass import utils
from olass.main import app

from olass.models.oauth_client_entity import OauthClientEntity
from olass.models.oauth_access_token_entity import OauthAccessTokenEntity

TOKEN_TYPE_BEARER = 'Bearer'

# TODO: read this options from config file
TOKEN_EXPIRES_SECONDS = 3600  # one hour
TOKEN_LENGTH = 40  # max 255

log = app.logger
oauth = OAuth2Provider(app)


@oauth.usergetter
def load_user():
    log.info("==> load_user()")
    return None


@oauth.clientgetter
def load_client(client_id):
    """
    This method is used by provider->authenticate_client()
    """
    return OauthClientEntity.query.filter_by(client_id=client_id).one()


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    tok = None

    if access_token:
        tok = OauthAccessTokenEntity.query.filter_by(
            access_token=access_token).one_or_none()
    elif refresh_token:
        tok = OauthAccessTokenEntity.query.filter_by(
            refresh_token=refresh_token).one_or_none()

    if tok:
        log.debug('Loaded token [{}] for user [{}]'.format(tok.id, tok.client))
    return tok


@oauth.tokensetter
def save_token(token_props, req, *args, **kwargs):
    """
    Saves token to the database
    """
    result_token = None
    token_id = token_props.get('id')
    token = OauthAccessTokenEntity.get_by_id(token_id)
    # log.debug("From {} got {}".format(token_id, token))

    if token and not token.is_expired():
        # log.debug("Reuse access token: {} expiring on {} ({} seconds left)"
        #           .format(token.id, token.expires, token.expires_in))
        result_token = token
    else:
        access_token = utils.generate_token()
        # access_token = utils.generate_token_urandom(TOKEN_LENGTH)
        expires = datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRES_SECONDS)
        added_at = utils.get_db_friendly_date_time()

        if token:
            result_token = OauthAccessTokenEntity.update(
                token,
                access_token=access_token,
                expires=expires,
                added_at=added_at)
        else:
            result_token = OauthAccessTokenEntity.create(
                access_token=access_token,
                token_type=TOKEN_TYPE_BEARER,
                _scopes='',
                expires=expires,
                client_id=req.client.client_id,
                added_at=added_at
            )
    # log.info("return from save_token: {}".format(result_token))
    return result_token


@app.route('/oauth/token', methods=['POST', 'GET'])
@oauth.token_handler
def handle_request_auth_token():
    """
    The dictionary returned by this method is passed to the meth:`save_token`
    in order to be saved
    """
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        client_secret = request.form.get('client_secret')
    else:
        client_id = request.args.get('client_id')
        client_secret = request.args.get('client_secret')

    if client_id is None:
        raise Exception("Error: Missing client_id")
    if client_secret is None:
        raise Exception("Error: Missing client_secret")

    client = OauthClientEntity.query.filter_by(
        client_id=client_id).one_or_none()

    if client is None:
        raise Exception("Error: invalid client_id")

    if client.client_secret != client_secret:
        raise Exception("Error: invalid client_secret")

    token = OauthAccessTokenEntity.query.filter_by(
        client_id=client_id,
        token_type=TOKEN_TYPE_BEARER).one_or_none()

    # log.info("return from handle_request_auth_token(): {}".format(token))
    return token.serialize() if token else {}


@oauth.grantgetter
def load_grant(client_id, code):
    log.debug("==> load_grant()")
    return None


@oauth.grantsetter
def save_grant(client_id, code, req):
    log.debug("==> save_grant()")
    return None
