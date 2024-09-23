from config import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.BigInteger, nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    user_password = db.Column(db.String(255), nullable=False)
    education = db.Column(db.String(255), nullable=True)
    profile_pic = db.Column(db.String(255), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='user')

    @property
    def password(self):
        raise AttributeError('Password Error')
    
    @password.setter 
    def password(self, value):
        self.user_password = generate_password_hash(value)

    def verify_password(self, value):
        return check_password_hash(self.user_password, value)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


