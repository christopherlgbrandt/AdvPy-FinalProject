from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure
from flask import Flask, render_template, request, redirect, url_for 

app = Flask(__name__)

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

def unFavorite(moviePoster, name, releaseDate, overview, reviewScore) -> None:
   """Unfavorites a movie
   """
   collection.delete_one({"Movie Poster": moviePoster, "Name": name, "Release Date": releaseDate,
                         "Overview": overview, "Review Score": reviewScore})

@app.route('/favorites')
def print_favorite():
   """Prints the list of favorite movies from MongoDB
   """
   result = collection.find()
   if result:
      movies = result.json()['results']
      return render_template('favorites.html', movies=movies)
   else:
      print("No results found :(")

#if __name__ == "__main__":
#   unFavorite("Some Jon Bois tweet or something", "17776", "Not 17776", "Football, but weird", "Hopefully a 10/10")
