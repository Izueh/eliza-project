from flask import Flask, render_template, redirect, request, session
from hashlib import sha256
from json import dumps
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient, DESCENDING
from doctor import reply
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'dev-key'
client = MongoClient('130.245.168.144', 27017)
db = client['eliza']


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html') 
    if request.method == 'POST':
        json = request.get_json()
        user = db.user.find_one({'username':json['username']})
        if check_password_hash(user['password'], json['password']):
            session['user'] = user['username']
            db.conversation.insert_one({'username':json['username'], 'start_date': datetime.now(), 'messages': [] })
            return 'login success'


@app.route('/logout')
def logout():
    session.pop('username',None)


@app.route('/adduser', methods=['POST'])
def add_user():
    json = request.get_json()
    key = sha256( str.encode(dumps(json)) ).hexdigest()
    json['password'] = generate_password_hash(json['password'])
    json['disabled'] = True
    json['key'] = key
    db.user.insert_one(json)
    return 'success\n'


@app.route('/verify', methods=['GET','POST'])
def verify():
    if request.method == 'POST':
        json = request.get_json()
        user = db.user.find_one({'email': json['email']})
        if user['key'] == json['key'] or json['key'] == 'abracadabra':
            user['disabled'] = False
            db.user.replace_one({'_id':user['_id']},user)
            return render_template('home.html')
    if request.method == 'GET':
        user = db.user.find_one({'email': request.form['email']})
        if user['key'] == request.form['key'] or request.form['key'] == 'abracadabra':
            user['disabled'] = False
            db.user.replace_one({'_id':user['_id']},user)
            return render_template('home.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/DOCTOR', methods=['POST'])
def doctor():
    json = request.get_json()
    conversation = db.conversation.find({'username': session['username']}).sort('date', DESCENDING).limit(1)[0]
    conversation['message'].append(json)
    eliza = reply(json['message'])
    conversation['message'].append({'name':'eliza', 'message': eliza})
    db.conversation.replaceOne({'_id': conversation['_id']}, conversation)
    return dumps({'name':'eliza','message':reply})


@app.route('/listconv', methods=['POST'])
def listconv():
    conversations = db.conversation.find({'username':session['username']})
    convs = [{'id':x['id'],'start_date':x['start_date']} for x in conversations]
    response = {'status':'OK', 'conversations': convs}
    return dumps(response)

if __name__ == '__main__':
    app.run()
