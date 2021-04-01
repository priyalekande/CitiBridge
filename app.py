import pymongo
import pprint
import requests
from pymongo import MongoClient
from flask_cors import CORS 
import re
from flask import Flask, render_template, request, redirect, url_for, session, jsonify


app = Flask(__name__)

app.secret_key = 'your secret key'


client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.hukag.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


db = client.feedGeneration

users = db.users





@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = users.count_documents({'name':'{}'.format(username)})
        if account>0:
            msg = 'Username account already exists!'    
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'     
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username should contain only alphabets and numbers'
        elif not username or not password or not email:
            msg = 'Please fill out the entire form !'
        else:
            user = {'username':'{}'.format(username), 'email':'{}'.format(email), 'password':'{}'.format(password)}
            users.insert_one(user)
            msg ='You have successfully registered !'
    
    elif request.method == 'POST':
        msg = 'Please fill entire form !'
    return render_template('register.html', msg =msg)


@app.route('/login', methods = ['GET', 'POST'])
def user_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        account = users.find_one({'name':'{}'.format(username), 'password':'{}'.format(password)})
        
        if account:
            session['username'] = username
            session['logged_in'] = True
            session['id'] = account['_id']
            
            msg = 'Login Successful!'
            
            return render_template('Menu.html', msg = msg)
        else:
            msg = 'Incorrect username or password!'
            return render_template('login.html', msg = msg)
    
    

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))     
                
        
        
    
#if __name__ == '__main__':
   # app.run(debug = False)

