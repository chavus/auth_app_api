from auth_api import db
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    hashed_password = db.Column(db.String)
    api_key = db.Column(db.String)
    role = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.hashed_password = generate_password_hash(password)
        self.api_key = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=16))


    def json(self):
        return {'id': self.id, 'username': self.username, 'api_key': self.api_key, 'role': self.role}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_apikey(cls, api_key):
        return cls.query.filter_by(api_key=api_key).first()


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
