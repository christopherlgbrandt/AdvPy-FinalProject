import requests
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure
from flask import Flask, render_template, request, redirect, url_for 
# Dependencies: requests, pymongo, flask

app = Flask(__name__)

path_to_certificate = './FinalProject.pem'

uri = "mongodb+srv://finalproject.d5uengt.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"

client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=path_to_certificate,
                     server_api=ServerApi('1'))

# Connecting TMBD API
tmdb_api_key = 'b4d93d832dedb548688fd7924b2fff85'

# let's connect to testDATA database I added in
db = client['favoriteMoviesDATA']

collection = db['favoriteMoviesCOLLECT']

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

@app.route('/search_movie')
def search_movie():
    # Example: Searching movies by a keyword
    search_query = request.args.get('query')
    tmdb_endpoint = f'https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={search_query}'
    
    # Make a request to TMDB API
    response = requests.get(tmdb_endpoint)
    if response.status_code == 200:
        movies = response.json()['results']
        return render_template('movies.html', movies=movies)
    else:
        return "Failed to fetch data from TMDB"
    
@app.route('/movie_info')
def movie_info():
    movie_id = request.args.get('movie_id')
    tmdb_result = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}&append_to_response=recommendations'

    response = requests.get(tmdb_result)
    if response.status_code == 200:
        movie = response.json()
        return render_template('info.html', movie=movie)
    else:
        return "failed to fetch data from TMDB"
    
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
   
def checkFavorite(moviePoster, name, releaseDate, overview, reviewScore) -> bool:
    """Checks to see if a movie is already in favorites

    Args:
        Everything relating to the movies to used to search

    Returns:
        bool: True or False on if the movie is in Mongodb
    """
    result = collection.find_one({"Movie Poster": moviePoster, "Name": name, "Release Date": releaseDate,
                                  "Overview": overview, "Review Score": reviewScore})
    return result is not None

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    # Get movie details from the request
    movie_data = request.json  # Assuming data is sent as JSON
    favorite(
        movie_data['Movie Poster'],
        movie_data['Name'],
        movie_data['Release Date'],
        movie_data['Overview'],
        movie_data['Review Score']
    )
    return "Movie added to favorites successfully!"

# Route for removing a movie from favorites
@app.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    # Get movie details from the request
    movie_data = request.json  # Assuming data is sent as JSON
    unFavorite(
        movie_data['Movie Poster'],
        movie_data['Name'],
        movie_data['Release Date'],
        movie_data['Overview'],
        movie_data['Review Score']
    )
    return "Movie removed from favorites successfully!"

@app.route('/favorites')
def print_favorite():
    """Prints the list of favorite movies from MongoDB"""
    result = collection.find()
    movies = list(result)  # Convert cursor to list of documents
    if movies:
        return render_template('favorites.html', movies=movies)
    else:
        return "No results found in favorites"

if __name__ == "__main__":
    app.run(debug=True)
