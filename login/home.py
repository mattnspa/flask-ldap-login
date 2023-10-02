from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('index', __name__)

@bp.route('/')
@bp.route('/index')
def index():
  user_info=None
  if current_user.is_authenticated:
    user_info = {
      'id':current_user.get_id()
    }
  return render_template('index.html', user=user_info)

@bp.route('/dashboard')
@login_required
def dashboard():
  user_info=None
  if current_user.is_authenticated:
    user_info = {
      'id':current_user.get_id()
    }
  return render_template('dashboard.html', user=user_info)