from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure

certificate = '/home/christopher/Documents/ClassesFall2023/CSCI310/FinalProject.pem'

uri = "mongodb+srv://finalproject.d5uengt.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"

client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=path_to_certificate,
                     server_api=ServerApi('1'))

db = client['testDB']
collection = db['testCol']
doc_count = collection.count_documents({})
print(doc_count) # Should print 0 as the testDB doesn't exist 

# let's connect to testDATA database I added in
db = client['testDATA']

collection = db['testCOLLECT']
doc_count = collection.count_documents({})

print(doc_count) # Should print 1 since their is one document in this collection
