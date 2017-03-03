from flask import Flask, render_template, redirect, request
from flask_login import current_user, login_user, LoginManager, login_required
from hashlib import sha256
from database import db
from json import dumps
from register import RegisterForm
from model.user import User

app = Flask(__name__)
app.secret_key = 'dev-key'
#address = 'postgresql://%s:%s@localhost:5432/eliza' % ('postgres', 'cse356')
#app.config['SQLALCHEMY_DATABASE_URI'] = address
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    pass


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first() # username can be any object property


@app.route('/login', methods=['POST'])
def login():
    form = RegisterForm()
    if request.method == "GET":
        return render_template('login.html', form=form)
    json = request.get_json()
    username = json['username']
    password = json['password']
    user = load_user(username) # queries db for user with 'username'
    if user:
        if user.check_passwd(password):
            login_user(user)
            # TODO YOU MUST NOW: 
            # delete any old cookies associated with this user in the db
            # since it's a new login, you now render a new session conversation
    else: 
        return "Invalid user"

#Temporary test
@app.route('/test')
@login_required
def test():
        # TODO execute db call to fetch the most recent conversation and render that
        return "you are a logged in user"

@app.route('/logout')


@app.route('/adduser', methods=['POST'])
def add_user():
    json = request.get_json()
    key = sha256( str.encode(dumps(json)) ).hexdigest()
    user = User(json['username'], json['password'], json['email'], key)
    db.session.add(user)
    db.session.commit()
    # msg = Message(key, sender='eliza@ramuh.com', recipients=[json['email']])
    # mail.send(msg)
    return "Added user"


@app.route('/eliza/DOCTOR', methods=['POST'])
def doctor():
    pass


if __name__ == '__main__':
    #db.init_app(app)
    #db.app = app
    #db.create_all()

    app.run()
