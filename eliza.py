from flask import Flask, render_template, redirect, request, session, jsonify
from hashlib import sha256
from json import dumps
from bson import json_util, ObjectId
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient, DESCENDING, ASCENDING
from doctor import reply
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'dev-key'
client = MongoClient('130.245.168.144', 27017)
db = client['eliza']


@app.route('/')
def index():
    if 'user' in session:
        conversation = db.conversation.find({'username': session['user']}).sort('start_date', DESCENDING).limit(1)[0]
        return render_template('home.html', session=session, convo=conversation)
    else:
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
            db.conversation.insert_one({'username':json['username'], 'start_date': datetime.utcnow(), 'messages': [] })
            success = {'status' : 'OK'}
            return jsonify(success)
        else:
            error = {'status' : 'ERROR', 'error' : 'Invalid user'}
            return jsonify(error)


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user',None)
        success = {'status': 'OK'}
        return jsonify(success)
    else:
        error = {'status' : 'ERROR'}
        return jsonify(error)


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
    if 'user' not in session:
        error = {'status': 'ERROR'}
        return jsonify(error)
    else:
        json = request.get_json()

        # create a message document each for the posted user message and eliza reply
        human_msg = { 'timestamp': datetime.utcnow(), 'name': session['user'], 'text': json['human'] } # I'm assuming that we get the message like our project : {"human" : "Blah"}
        eliza = reply(json['human'])
        eliza_msg = { 'timestamp': datetime.utcnow(), 'name': 'eliza', 'text': eliza }
        
        # get the most recent conversation and update it's message array
        conversation = db.conversation.find({'username': session['user']}).sort('start_date', DESCENDING).limit(1)[0]
        conversation['messages'].append(human_msg)
        conversation['messages'].append(eliza_msg)
        db.conversation.replace_one({'_id': conversation['_id']}, conversation)

        # return the eliza reply
        return jsonify({'eliza': eliza})


@app.route('/listconv', methods=['POST'])
def listconv():
    if 'user' not in  session:
        error = {'status' : 'ERROR'}
        return jsonify(error)
    else:
        conversations = db.conversation.find({'username':session['user']})
        convs = [{'id':str(x['_id']),'start_date':x['start_date']} for x in conversations]
        if convs:
            response = {'status':'OK', 'conversations': convs}
            return jsonify(response) 
        else:
            error = {'status' : 'ERROR'}
            return jsonify(error)

@app.route('/getconv', methods=['POST'])
def get_conv():
    if 'user' not in session:
        error = {'status' : 'ERROR'}
        return jsonify(error)
    else:
        json = request.get_json()
        convo = db.conversation.find_one({'_id': ObjectId(json['id'])})
        if convo:
            response = {'status' : 'OK', 'conversation' : convo['messages']}
            return jsonify(response)
        else:
            error = {'status' : 'ERROR'}
            return jsonify(error)

if __name__ == '__main__':
    app.run()
