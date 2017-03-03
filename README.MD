# Eliza
A REST based web-app based on the the original ELIZA chatbot

## Run:
```
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
sudo apt install python3-dev postgresql postgresql-contrib postgresql-server-dev-all
pip install -r requirements.txt
python3 eliza.py
```

## Testing the Chatbot
You can test the Eliza chatbot by running
```
$ python3 -i doctor.py
```
and in the Python 3 shell, call
```
>>> reply("Hello Eliza")
```
