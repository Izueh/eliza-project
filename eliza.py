from flask import Flask, render_template, redirect, request, session
from hashlib import sha256
from json import dumps
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'dev-key'
client = MongoClient('130.245.168.144', 27017)
db = client['eliza']

@app.route('/')
def index():
    pass


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        json = request.get_json()
        user = db.user.find_one({'username':json['username']})
        if check_password_hash(user['password'], json['password']):
            session['user'] = user
            return 'login success'

@app.route('/logout')
def logout():
    session.pop('username',None)





@app.route('/adduser', methods=['POST'])
def add_user():
    json = request.get_json()
    key = sha256( str.encode(dumps(json)) ).hexdigest()
    json['password'] = generate_password_hash(json['password'])
    db.user.insert_one(json)
    return 'success\n'



@app.route('/eliza/DOCTOR', methods=['POST'])
def doctor():
    pass


if __name__ == '__main__':
    app.run()
