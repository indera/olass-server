"""
Goal: Define a generic page for the index

@authors:
  Andrei Sura <sura.andrei@gmail.com>
"""

import uuid
from flask import current_app
from flask import url_for
from flask import redirect
from flask import request
from flask import session
from flask import render_template

from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user

from wtforms import Form, TextField, PasswordField, HiddenField, validators
from flask_principal import \
    Identity, AnonymousIdentity, identity_changed, identity_loaded, RoleNeed

from olass import utils
from olass.main import app
# from olass.models.partner_entity import PartnerEntity
from olass.models.oauth_user_entity import OauthUserEntity


log = app.logger
# set the login manager for the app
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_message = ""
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    """Return the user from the database"""
    return OauthUserEntity.get_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    """ Returns a message for the unauthorized users """
    # return redirect('/')
    return 'Please <a href="{}">login</a> first.'.format(url_for('index'))


class LoginForm(Form):
    """ Declare the validation rules for the login form """
    next = HiddenField(default='')

    # email = TextField('Email', [validators.Length(min=4, max=25)])
    email = TextField('Email')
    password = PasswordField(
        'Password', [
            validators.Required(), validators.Length(
                min=8, max=50)])


@app.before_request
def check_session_id():
    """
    Generate a UUID and store it in the session.
    """
    if 'uuid' not in session:
        session['uuid'] = str(uuid.uuid4())


@app.route('/', methods=['POST', 'GET'])
def index():
    """
    Render the login page with username/pass

    """
    if current_user.is_authenticated:
        log.debug("Redirect authenticated user: {}".format(current_user))
        return redirect(url_for('say_hello'))

    # uuid = session['uuid']
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        email = form.email.data.strip() if form.email.data else ""
        password = form.password.data.strip() if form.password.data else ""
        user = OauthUserEntity.query.filter_by(email=email).one_or_none()

        if user:
            log.debug("Found user object: {}".format(user))
        else:
            utils.flash_error("No such email: {}".format(email))
            log.debug("Redirect no such email: {}".format(email))
            return redirect(url_for('index'))

        if user.verify_password(password):
            log.debug('Successful login for: {}'.format(user))
            login_user(user, remember=False, force=False)

            # Tell Flask-Principal that the identity has changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.get_id()))
            return redirect(url_for('say_hello'))
        else:
            log.debug('Incorrect password for: {}'.format(user))
            utils.flash_error("Incorrect username/password.")

    # When sending a GET request render the login form
    return render_template('index.html', form=form,
                           next_page=request.args.get('next'))


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    """ Describe what `needs` are provided by this identity
    @TODO: add unit tests
stackoverflow.com/questions/16712321/unit-testing-a-flask-principal-application
    """
    if type(current_user) == 'AnonymousUserMixin':
        return

    identity.user = current_user

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            # log.debug("Provide role: {}".format(role))
            identity.provides.add(RoleNeed(role.name))


@app.route('/logout')
def logout():
    """
    Destroy the user session and redirect to the index page
    """
    if 'uuid' in session:
        log.info("Logout: {}".format(session['uuid']))

    logout_user()

    # Remove session keys set by Flask-Principal, and `uuid` key set manually
    for key in ('identity.name', 'identity.auth_type', 'uuid'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect('/')
