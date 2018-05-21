from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager

# 加载用户的回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """
    uid             用户id



    username        用户昵称
    password_hash   密码哈希
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)


class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)
    tags = db.Column(db.String(256))
    abstract = db.Column(db.String(256))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
