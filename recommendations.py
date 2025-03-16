import pandas as pd
import pickle
import requests
import os
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# Load movie data
movies = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies)
similarity = pickle.load(open('similarity.pkl', 'rb'))


# Movie Recommendation System Functions
def fetch_movie_details(movie_title):
    response = requests.get(f"http://www.omdbapi.com/?i=tt3896198&t={movie_title}&apikey={OMDB_API_KEY}")
    movie_data = response.json()
    poster_url = movie_data.get('Poster')
    title = movie_data.get('Title', 'N/A')
    year = movie_data.get('Year', 'N/A')
    genre = movie_data.get('Genre', 'N/A')
    imdb_rating = movie_data.get('imdbRating', 'N/A')
    plot = movie_data.get('Plot', 'N/A')
    imdb_id = movie_data.get('imdbID', 'N/A')

    return {
        "poster_url": poster_url,
        "title": title,
        "year": year,
        "genre": genre,
        "imdb_rating": imdb_rating,
        "plot": plot,
        "imdb_id": imdb_id
    }


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommendations = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        details = fetch_movie_details(movie_title)
        recommendations.append(details)

    return recommendations