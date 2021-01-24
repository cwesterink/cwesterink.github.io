from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    image = db.Column(db.BLOB,default=None)
    # joined_at = db.Column(db.DateTime(), default = datetime.utcnow, index = True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_image(self, image):
        self.image = image
