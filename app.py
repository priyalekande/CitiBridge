import pymongo
import pprint
from flask import request, make_response, jsonify
from pymongo import MongoClient
from flask_cors import CORS 
import re
import numpy as np
import pandas as pd
from decimal import *
import io
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_accept import accept
import csv
import datetime



app = Flask(__name__)

app.secret_key = 'your secret key'

# if __name__ == '__main__':
#    app.run(debug = False)

client = pymongo.MongoClient("mongodb+srv://host:host@cluster0.6o0pa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


db = client.ClearingFeedGenerationSystem

users = db.user



@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/register', methods =['GET', 'POST'])
def register():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    msg = ''
    data = request.json
    if request.method == 'POST' and 'username' in data and 'password' in data and 'email' in data:
        username = data['username']
        password = data['password']
        email = data['email']
        account = users.count_documents({'username':'{}'.format(username)})
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
    response = jsonify({
        "msg": msg
    })
    return response


@app.route('/login', methods = ['GET', 'POST'])
def user_login():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    msg = ''
    data = request.json
    if request.method == "POST":
        username = data["username"]
        # email = data["email"]
        password = data["password"]
        
        account = users.find_one({"username": username, "password": password})
        
        if account:
            session['username'] = username
            session['logged_in'] = True
            # session['id'] = account['_id']
            msg = 'Login succcessful' 
        else:
            msg = 'Login Unsuccessful'
    response = jsonify({
        "msg": msg
    })    
    return response
    
    

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    # session.pop('id', None)
    session.pop('username', None)
    msg = 'Logged out'
    return msg

#############################################################################################

@app.route('/upload', methods = ['GET', 'POST'])
#@accept('multipart/form-data')
def transactions():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")

    #df = pd.read_csv(request.files.get('file'))
    # f = request.form.get('csv_file')
    # #f = request.files["csv_file"]
    
    # if f.filename != '':
    #      f.save(f.filename)

    # #data = []

    #data = request.files['csv_file'].read()
#     with open('D:\CitiBridge-dev\data.csv', mode ='r')as file: 
      
#     # reading the CSV file 
#     csvFile = csv.reader(file) 
    
#   # displaying the contents of the CSV file 
#     for lines in csvFile: 
#         print(lines) 
#     print(data,"\n\n")
    #with open('employee_birthday.txt') as csv_file:
    #csv_reader = csv.reader(f, delimiter=',')
    #line_count = 0
    #   if line_count == 0:
    #         print(f'Column names are {", ".join(row)}')
    #         line_count += 1
    #     else:
    #         print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
    #         line_count += 1
    # print(f'Processed {line_count} lines.')
    # csvfile = csv.reader(f)
    # for row in csvfile:
    #     data.append(row)
    # print("\n",data,"\n")  
  
    #df = pd.DataFrame(data)
    df = pd.read_csv("D:\CitiBridge-dev\data.csv")
    # print(df)

    # new_header = df.iloc[0] 
    # #df = df[1:] 
    # df.columns = new_header 
    # print("df.columns")
    # print(df.columns,"\n")
    # df.reset_index(drop=True, inplace=True)

    # df = pd.read_csv(f)
    print(df)

    df["index_col"] = df.index
    df = df.set_index("index_col")
    print(df.columns)

    df.amount = df.amount.astype(float)

    df.payeeacc = df.payeeacc.astype(str)

    parts1 = []
    parts2 = []
    parts3 = []

    for str1 in df["transactionrefpayername"]:
        indices = [0, 12, 20]
        parts = [str1[i:j] for i, j in zip(indices, indices[1:] + [None])]
        parts1.append(parts[0])
        parts2.append(parts[1])
        parts3.append(parts[2])

    data = {"transactionref": parts1, "date": parts2, "payer": parts3}
    df1 = pd.DataFrame(data)

    parts1 = []
    parts2 = []

    for str1 in df["payeraccpayee"]:
        indices = [0, 12]
        parts = [str1[i:j] for i, j in zip(indices, indices[1:] + [None])]
        parts1.append(parts[0])
        parts2.append(parts[1])

    df1["payeracc"] = parts1
    df1["payee"] = parts2

    df1["payeeacc"] = df["payeeacc"]
    df1["amount"] = df["amount"]
    print(df1)
    # df1 is the final dataframe

    list_of_col = [
        df1["transactionref"],
        df1["payer"],
        df1["payeracc"],
        df1["payee"],
        df1["payeeacc"],
    ]

    def date_validation(day, month, year):
     
        isValidDate = True
     
        try :
            datetime.datetime(year, month, day)
         
        except ValueError :
            isValidDate = False
         
        if(isValidDate) :
            return True
        else :
           return False

    def date_format(date):
        return(date[0:2]+"-"+date[2:4]+"-"+date[4:])


    def validating_rows(x):
        transactionref = x["transactionref"]
        # print(transactionref)
        payer = x["payer"]
        payeracc = x["payeracc"]
        payee = x["payee"]
        payeeacc = x["payeeacc"]
        amount = x["amount"]
        date = x["date"]
        date_str = date.str
        
        if(
            transactionref.str.isalnum
            and payer.str.isalnum
            and payeracc.str.isalnum
            and payee.str.isalnum
            and payeeacc.str.isalnum
            and date_validation(int(date_str[0:2]),int(date_str[2:4]),int(date_str[4:]))
        ):
            x["validate"] = "Pass"
            x["Date"] = date_format(date_str)
        else:
            x["validate"] = "Fail"
            x["Date"] = "Invalid date"
        return x


    df1 = df1.groupby(level=0).apply(validating_rows)
    del df1["date"]
    df1 = df1[["transactionref","Date","payer","payeracc","payee","payeeacc","amount","validate"]]
    df1.to_csv(r"D:\transactions.csv")
    print(df1)
    data = df1.to_dict('list')
    session['data'] = data


    # Database - ClearingFeedGeneration
    db = client.get_database("ClearingFeedGenerationSystem")

    # Collection - Transaction
    records = db.transaction

    data_dict = df1.to_dict("records")
    # Insert collection
    records.insert_many(data_dict)

    for i in range(len(data_dict)):
        del data_dict[i]['_id']
    
    response = jsonify({
        "records": data_dict
    })
    return response


# @app.route('/csv')  
# def download_current_csv(df):
#     dw = session.get('data') # get the current uploaded csv
#     df = pd.DataFrame(dw) # convert to dataframe
  
#     print(df)
#     resp = make_response(df.to_csv()) 
#     resp.headers["Content-Disposition"] = "attachment; filename=transactions.csv"
#     resp.headers["Content-Type"] = "text/csv"
#     return resp

# @app.route('/csv_history/')  
# def download_history_csv():
#     user_name = session.get('username')
#     connection_url = "mongodb+srv://host:host@cluster0.6o0pa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
#     client = pymongo.MongoClient(connection_url)

#     # Database - ClearingFeedGeneration
#     db = client.get_database("ClearingFeedGenerationSystem")

#     # Collection - Transaction
#     records = db.transaction

#     temp_list = []
#     for i in records.find({'user':'{}'.format(user_name)}):
#         temp_list.append(i)
#     df = pd. DataFrame(temp_list)
#     df =df.drop(['_id','user'], axis =1)
#     order = ['tans_ref','amount','payer_acc', 'payer_name', 'payee_acc', 'payee_name', 
#         'value_date','status']
#     df = df[order]
#     resp = make_response(df.to_csv()) 
#     resp.headers["Content-Disposition"] = "attachment; filename=transactions.csv"
#     resp.headers["Content-Type"] = "text/csv"
#     return resp
  
