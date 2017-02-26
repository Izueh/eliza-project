from flask import Flask, render_template, redirect, request
from flask_login import current_user, login_user, LoginManager
from hashlib import sha256
from werkzeug.security import check_password_hash, generate_password_hash, _hash_funcs
from flask_mail import Message
from mail import mail
from database import db
from json import dumps
from os import environ
from model.user import User

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
    return s


@app.route('/login', methods=['POST'])
def login():
    json = request.get_json()
    user = json['username']
    password = json['password']
    try_auth = User.get(username) # queries db for user with 'username'
    if try_auth:
        if check_password_hash(password, try_auth['password']):
            login_user(try_auth)
            # TODO YOU MUST NOW: 
            # delete any old cookies associated with this user in the db
            # since it's a new login, you now render a new session conversation
    else: 
        return "Invalid user"

#Temporary test
@app.route('/test')
@login_required
def test():
    if current_user.is_authenticated():
        # TODO execute db call to fetch the most recent conversation and render that
        return "you are a logged in user"

@app.route('/logout',)


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


@app.route('/eliza/DOCTOR', methods=['POST'])
def doctor():
    pass


if __name__ == '__main__':
    app.run()
