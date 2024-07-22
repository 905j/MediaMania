from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    media_id = db.Column(db.Integer, nullable=False)
    media_type = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    poster_path = db.Column(db.String(200), nullable=True)
    vote_average = db.Column(db.Float, nullable=True)
    rating = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<Favorite {self.title}>'

class MediaRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    media_id = db.Column(db.Integer, nullable=False)
    media_type = db.Column(db.String(10), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref=db.backref('ratings', lazy=True))

    def __repr__(self):
        return f'<MediaRating {self.user_id} {self.media_id} {self.media_type} {self.rating}>'