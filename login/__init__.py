from flask import Flask, current_app
from flask_login import LoginManager

login_manager = LoginManager()

def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True,template_folder='templates')

    # Load default config
    app.config.from_object('config.default')
    # Load config from instance folder
    app.config.from_pyfile('config.py')
    # Load config from file specified by APP_CONFIG_FILE env var
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .auth.auth import bp as auth
    app.register_blueprint(auth)
    from .home import bp as home
    app.register_blueprint(home)

    return app