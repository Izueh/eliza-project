from flask import Flask, render_template, redirect, request
from flask_login import current_user, login_user, LoginManager
from hashlib import sha256
from werkzeug.security import check_password_hash, generate_password_hash, _hash_funcs
from flask_mail import Message
from mail import mail
from database import db
from json import dumps
from os import environ

app = Flask(__name__)
app.secret_key = 'dev-key'
mail.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    pass


@login_manager.user_loader
def load_user(user_id):
    pass


@app.route('/login', methods=['POST'])
def login():
    pass


@app.route('/eliza/DOCTOR', methods=['POST'])
def doctor():
    pass


@app.route('/adduser', methods=['POST'])
def add_user():
    json = request.get_json()
    key = sha256(dumps(json)).hexdigest()
    db.put('users', json['username'], {
        'password': generate_password_hash(json['password']),
        'email': json['email'],
        'activated': False,
        'key': key
    })
    msg = Message(key, sender='eliza@ramuh.com', recipients=[json['email']])
    mail.send(msg)


if __name__ == '__main__':
    app.run()
