#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, jsonify, request
from flask_cors import CORS
import pymongo


# In[2]:


connection_url = 'mongodb+srv://host:host@cluster0.6o0pa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
app = Flask(__name__)
client = pymongo.MongoClient(connection_url)


# In[3]:


#Database - ClearingFeedGeneration
db = client.get_database('ClearingFeedGenerationSystem')

#Collection - Transaction
records = db.transaction


# In[4]:


username = "xyz" #currently active user


# In[5]:


#Getting all transactions related to the user

@app.route('/', methods=['GET'])
def User():
	query = records.find({"user": username})
	output = {}
	i = 0
	for x in query:
		output[i] = x
		output[i].pop('_id')
		i += 1
	return jsonify(output)


# In[6]:


#search by Transaction Id

@app.route('/searchId/<id>/', methods=['GET'])
def SearchId(id):
	query = records.find_one({"tans_ref": id})
	query.pop('_id')
	return jsonify(query)


# In[8]:


if __name__ == '__main__':
	app.run(debug=False)


# In[ ]:




