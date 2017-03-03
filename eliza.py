from flask import Flask, render_template, redirect, request, session
from hashlib import sha256
from json import dumps
from model.user import User

app = Flask(__name__)
app.secret_key = 'dev-key'


@app.route('/')
def index():
    pass


def load_user(user_id):
    return User.query.filter_by(username=user_id).first() # username can be any object property


@app.route('/login', methods=['GET','POST'])
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
            session['username']=username
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
def logout():
    session.pop('username',None)





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
    db.init_app(app)
    db.app = app
    db.create_all()

    app.run()
