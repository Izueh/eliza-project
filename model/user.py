from flask_login import UserMixin
from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'euser'
    username = db.Column(db.String(14), primary_key=True)
    password = db.Column(db.String(256))
    email = db.Column(db.String(50),unique=True)
    validated = db.Column(db.BOOLEAN)
    key = db.Column(db.String(256))

    def __init__(self, username, password, email,key):
        self.username=username
        self.password=generate_password_hash(password)
        self.email= email
        self.validated= False
        self.key=key

    def check_passwd(self,passwd):
        return check_password_hash(self.password,passwd)

    def get_id(self):
        return self.username


