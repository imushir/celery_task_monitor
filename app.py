import re
import json
import time
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template, \
                 request, redirect, url_for, session, json
from pymongo import MongoClient
import jwt
from functools import wraps

app = Flask(__name__)
app.secret_key = 'dummykey'
DB_NAME = "CeleryTask"
MONGODB_URL = "mongodb://localhost:27017/"
db_client = MongoClient(MONGODB_URL)
db_object = db_client[DB_NAME]
celery_meta_collec = db_object["celery_taskmeta"]
users_auth_collec = db_object["auth_users"]

#------- table record format ---------------
"""
data = [{
  "status": "SUCESS",
  "result": "10",
  "date_done": "2021-02-26T15:43:08.529088"
  
}]
"""
def token_required(wrap_func): 
    @wraps(wrap_func) 
    def token_decoding(*args, **kwargs): 
        token = ""
        # jwt is passed in the request header
        if ("access-token") in session:
            token =session["access-token"]
        if not token: 
            return jsonify({'Message' : 'Token is required'}), 401
        try: 
            # decoding the payload to fetch the stored details
            jwt_response = jwt.decode(token, app.config['SECRET_KEY'],
                                  options={"verify_signature": False})
        except Exception as jwt_err:
            print('JWT decode error ', jwt_err)
            return jsonify({ 
                'Message' : 'Token is invalid'
            }), 401
        return  wrap_func(*args, **kwargs) 
   
    return token_decoding

def get_celery_record():
  celery_records = celery_meta_collec.find({}, {"_id": False, 
                                              "traceback": False,
                                              "children": False})
  table_data = []
  for each_record in celery_records:
      table_data.append(each_record)
  return table_data


def validate_login(email_id, password):                                            
  user_record = users_auth_collec.find_one({"user_emailid": email_id,
                                            "user_pass": password})
  if user_record:
    return user_record
  return False


@app.route('/celery_monitor')
@token_required
def celery_monitor():
    if("loggedin" in session):
        table_header = [
                    {
                      "field": "status", 
                      "title": "status",
                      "sortable": True,
                    },
                    {
                      "field": "result",
                      "title": "result",
                      "sortable": True,
                    },
                    {
                      "field": "date_done",
                      "title": "date_done",
                      "sortable": True,
                    },
                    ]
        celery_response = get_celery_record()
        return render_template("celery_monitor.html",
                                 data=celery_response,
                                 columns=table_header,
                                 title='Celery Task Monitor')
    else:
        return redirect(url_for('login'))


@app.route('/') 
@app.route('/login', methods =['GET', 'POST']) 
def login():
    msg = '' 
    if request.method == 'POST' and 'username' in request.form \
                                and 'password' in request.form:
        username = request.form['username'] 
        password = request.form['password']
        response_record = validate_login(username, password)
        if response_record:
            try:
                user_id = str(response_record['_id'])
                session['loggedin'] = True
                session['id'] = user_id
                session['username'] = response_record['user_emailid']
                token = jwt.encode({'access_id': user_id, 
                                    'exp': datetime.utcnow() \
                                    + timedelta(minutes = 30)},
                                    app.config['SECRET_KEY'])
                session['access-token'] = token
                print("login token ", token)
            except Exception as err:
                print("Exception is ", err)
            return redirect(url_for('celery_monitor'))
        else: 
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
  
@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('username', None) 
    return redirect(url_for('login')) 
  
@app.route('/register', methods =['GET', 'POST']) 
def register(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and \
                  'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password'] 
        email = request.form['email']
        response_record = validate_login(email, password)
        if response_record:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            usr_doc = {"user_emailid":email,
                        "user_pass": password,
                        "user_name": username,
                        "user_role": "nonadmin"} 
            users_auth_collec.insert_one(usr_doc)
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg) 

if __name__ == '__main__':
  app.run(debug=True)