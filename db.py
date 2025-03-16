import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def connect_to_postgresql():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def create_tables():
    conn = connect_to_postgresql()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(256) NOT NULL,
            role VARCHAR(10) NOT NULL
        );
    ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS watchlist (
                id SERIAL PRIMARY KEY, 
                username VARCHAR(50) NOT NULL, 
                movie_name TEXT NOT NULL,
                poster_url TEXT,
                genre VARCHAR(50),
                year INTEGER,
                imdb_rating FLOAT
            );
        ''')
    conn.commit()
    conn.close()


# Add a movie to the watchlist
def add_to_watchlist(username, movie_name, poster_url, genre, year, imdb_rating):
    conn = connect_to_postgresql()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO watchlist (username, movie_name, poster_url, genre, year, imdb_rating) VALUES (%s, %s, %s, %s, %s, %s)",
        (username, movie_name, poster_url, genre, year, imdb_rating)
    )
    conn.commit()
    conn.close()


# Remove a movie from the watchlist
def remove_from_watchlist(username, movie_name):
    conn = connect_to_postgresql()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM watchlist WHERE username = %s AND movie_name = %s",
        (username, movie_name)
    )
    conn.commit()
    conn.close()


# Fetch movies from the watchlist of a specific user
def get_watchlist(username):
    conn = connect_to_postgresql()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, movie_name, poster_url, genre, year, imdb_rating FROM watchlist WHERE username = %s",
        (username,)
    )
    watchlist = cursor.fetchall()
    conn.commit()
    conn.close()
    return watchlist

