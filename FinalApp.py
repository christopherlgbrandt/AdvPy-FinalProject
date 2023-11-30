import requests
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure
from flask import Flask, render_template, request, redirect, url_for 

app = Flask(__name__)

path_to_certificate = '/home/christopher/Documents/ClassesFall2023/CSCI310/FinalProject.pem'

uri = "mongodb+srv://finalproject.d5uengt.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"

client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=path_to_certificate,
                     server_api=ServerApi('1'))

# Connecting TMBD API
tmdb_api_key = 'b4d93d832dedb548688fd7924b2fff85'

# let's connect to testDATA database I added in
db = client['testDATA']

collection = db['testCOLLECT']

# the comment below can be used for testing to make sure your connected to the database.
# doc_count = collection.count_documents({})

# print(doc_count) # Should print 1 since their is one document in this collection

@app.route('/')
def index():
    # Retrieve data from MongoDB
    data = list(collection.find())
    return render_template('index.html', data=data)

@app.route('/add', methods=['POST'])
def add_task():
    data_content = request.form['content']
    new_data = {'content': data_content}

    # Insert new data into MongoDB
    collection.insert_one(new_data)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)