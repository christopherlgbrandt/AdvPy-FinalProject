from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure

uri = "mongodb+srv://finalproject.d5uengt.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='FinalProject.pem',
                     server_api=ServerApi('1'))

db = client['favoriteMoviesDATA']
collection = db['favoriteMoviesCOLLECT']

def favorite(name, releaseDate, overview) -> None:
   """Allows one to "favorite" a movie saving
      it to a database on MongoDB
   """
   favMovie = {"Name": name, "Release Date": releaseDate, "Overview": overview}
   collection.insert_one(favMovie)

def print_favorite() -> None:
   result = collection.find()
   if result:
      for doc in result:
         name = doc['Name']
         releaseDate = doc['Release Date']
         overview = doc['Overview']
         print(f'{name} was released on {releaseDate} and a quick overview is:\n{overview}')
   else:
      print("No results found :(")

if __name__ == "__main__":
   #favorite("idk", "idk", "idk")
   print_favorite()
