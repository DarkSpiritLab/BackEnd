from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config, QQ_APP_ID, QQ_APP_KEY
from flask_login import LoginManager
from flask_openid import OpenID
from flask_oauthlib.client import OAuth
from flask_principal import Principal, Permission, RoleNeed, identity_loaded
from flask_celery import Celery
from flask_socketio import SocketIO


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
oid = OpenID()
celery = Celery()
principal = Principal()
socketio = SocketIO()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

oauth = OAuth()
qq = oauth.remote_app(
    'qq',
    consumer_key=QQ_APP_ID,
    consumer_secret=QQ_APP_KEY,
    base_url='https://graph.qq.com',
    request_token_url=None,
    request_token_params={'scope': 'get_user_info'},
    access_token_url='/oauth2.0/token',
    authorize_url='/oauth2.0/authorize',
)


def create_app(config_name):
    # 初始化配置
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 注册方法
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    oid.init_app(app)
    oauth.init_app(app)
    principal.init_app(app)

    from .api import api as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint)
    # 注册蓝图

    socketio.init_app(app)
    return app
