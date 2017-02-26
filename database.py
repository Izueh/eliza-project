from hyperdex import client, admin

db = client.Client(environ['DB_IP'], environ['DB_PORT'])
admin = admin.Admin(environ['DB_IP'], environ['DB_PORT'])

if __name__ == '__main__':
    admin.add_space('''
    space user
    key username
    attributes password, email, activated, key
    tolerate 2 failures
    ''')
    admin.add_space('''
    space user_session
    key cookie
    attributes user_id
    ''')
    admin.add_space('''
    space conversations
    key convo_num
    attributes messages
    ''')
