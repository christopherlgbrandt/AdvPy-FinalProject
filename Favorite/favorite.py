from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure

uri = "mongodb+srv://finalproject.d5uengt.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='../FinalProject.pem',
                     server_api=ServerApi('1'))

db = client['favoriteMoviesDATA']
collection = db['favoriteMoviesCOLLECT']

def favorite() -> None:
    """Allows one to "favorite" a movie saving
       it to a database on MongoDB
    """
    favMovie = {"Name": "Test", "Release Date": "17776", "Overview": "Test"}
    collection.insert_one(favMovie)
