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

def favorite(moviePoster, name, releaseDate, overview, reviewScore) -> None:
   """Allows one to "favorite" a movie saving
      it to a database on MongoDB
   """
   favMovie = {"Movie Poster": moviePoster, "Name": name, "Release Date": releaseDate,
               "Overview": overview, "Review Score": reviewScore}
   collection.insert_one(favMovie)

def print_favorite() -> None:
   result = collection.find()
   if result:
      for doc in result:
         moviePoster = doc['Movie Poster']
         name = doc['Name']
         releaseDate = doc['Release Date']
         overview = doc['Overview']
         reviewScore = doc['Review Score']
         print(f'Movie Poster: {moviePoster}\n{name} was released on {releaseDate} and a quick overview is:\n{overview}\nIts total review score is {reviewScore}.')
   else:
      print("No results found :(")

if __name__ == "__main__":
   favorite("Some Jon Bois tweet or something", "17776", "Not 17776", "Football, but weird", "Hopefully a 10/10")
   print_favorite()
