from datetime import datetime

from .  import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_admin._compat import as_unicode

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    image = db.Column(db.BLOB,default=None)
    gender = db.Column(db.String,default="Unknown")
    bio = db.Column(db.String(), default='')
    status = db.Column(db.String(), default="member")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_image(self, image):
        self.image = image

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id








class History(db.Model):
    id = db.Column("id", db.Integer,primary_key=True)
    message = db.Column("message", db.String())
