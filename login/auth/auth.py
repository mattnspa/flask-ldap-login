from flask import Blueprint, flash, g, redirect, render_template, request, url_for, current_app
from flask_login import current_user, login_required, login_user, logout_user

from .. import login_manager
from .models import User
from .form import LoginForm

bp = Blueprint('auth', __name__)

def validate_and_login_user(username, password):
  from .. import ldap as ldap_helper
  id = ldap_helper.login(username,password)
  if id:
    return login_user(User(id))
  return False


@login_manager.user_loader
def load_user(user_id):
  from .. import ldap as ldap_helper
  print('Loading user: {}'.format(user_id))
  id = ldap_helper.service_get_id('(uidNumber={})'.format(user_id))
  if id:
    print('User id found')
    return User(id)
  print('User not found')
  return None

@bp.route('/login', methods=['GET', 'POST'])
def login():

  if current_user.is_authenticated:
    flash('You are already logged in.')
    return redirect(url_for('index.index'))

  form = LoginForm()
  if form.validate_on_submit():
    print('valid form, authenticating')
    if validate_and_login_user(form.user_name.data,form.password.data):
      flash('Logged in successfully.')
      next = request.args.get('next')
      # url_has_allowed_host_and_scheme should check if the url is safe
      # for redirects, meaning it matches the request host.
      # See Django's url_has_allowed_host_and_scheme for an example.

      # if not url_has_allowed_host_and_scheme(next, request.host):
      #     return flask.abort(400)

      return redirect(next or url_for('index.index'))
    flash('Unable to log in')
  return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.index'))