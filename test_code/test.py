from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://finalproject.d5uengt.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='../X509-cert-6268247238609712663.pem',
                     server_api=ServerApi('1'))

db = client['testDB']
collection = db['testCol']
doc_count = collection.count_documents({})
print(doc_count)
