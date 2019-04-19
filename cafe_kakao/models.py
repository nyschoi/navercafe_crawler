from datetime import datetime
from cafe_kakao import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    kakaoid = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    access_token = db.Column(db.String(100))
    refresh_token = db.Column(db.String(100))
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.kakaoid}', '{self.username}', '{self.access_token}', '{self.refresh_token}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clubid = db.Column(db.String(100), nullable=False)
    menuid = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(100))

    def __repr__(self):
        return f"Post('{self.clubid}', '{self.menuid}', '{self.date_posted}', '{self.description}')"
