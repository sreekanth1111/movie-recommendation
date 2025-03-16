import time

import streamlit as st
from auth import add_user, validate_user
from recommendations import recommend, movies
from db import add_to_watchlist


movies_title = movies['title'].values


# Load external CSS
def add_custom_css():
    with open("css/styles.css", "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# Authentication Functions
def signup():
    st.title("🔑 Sign Up")
    st.write("---")
    role = st.selectbox("Select Role", ["Admin", "User"])
    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")
    confirm_password = st.text_input("🔄 Confirm Password", type="password")
    if st.button("Create Account", key="signup_submit"):
        if username and password and confirm_password:
            if password == confirm_password:
                add_user(username, password, role)
                st.session_state["view"] = "login"
                st.rerun()
            else:
                st.error("Passwords do not match!")
        else:
            st.error("Please fill out all fields.")


def login():
    st.title("🔐 Login")
    st.write("---")
    role = st.selectbox("Select Role", ["Admin", "User"])
    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")
    if st.button("Login", key="login_submit"):
        user = validate_user(username, password, role)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = role
            st.session_state["view"] = "homepage"
            st.session_state["show_dashboard"] = False
            st.success(f"Logged in as {username} ({role}). Redirecting to movie recommendations...")
            st.rerun()
        else:
            st.error("Invalid credentials!")

def add_movie_to_watchlist(movie_data):
    if movie_data["title"] not in st.session_state["watchlist"]:
        st.session_state["watchlist"].append(movie_data["title"])
        add_to_watchlist(st.session_state["username"], movie_data["title"], movie_data["poster_url"], movie_data['genre'], movie_data['year'], movie_data['imdb_rating']) 
        st.write("\n" * 2)
        st.success(f"{movie_data['title']} added to your watchlist!")
        time.sleep(2)
        st.session_state["view"] = "watchlist"
    else:
        st.warning(f"{movie_data['title']} is already in your watchlist.")



def show_movie_recommendations():
    st.title('🎬 Movie Recommendation System')

    # Search bar input
    movie_query = st.text_input("Search for a movie:", "")

    # If a search query is provided, show matching suggestions
    if movie_query:
        suggestions = [movie for movie in movies_title if movie_query.lower() in movie.lower()]
        if suggestions:
            selected_movie = st.selectbox("Select a movie:", suggestions)
        else:
            st.write("No matching movies found.")
            selected_movie = movie_query  # Use the query itself if no suggestions found
    else:
        # If no search query, show the default selectbox with all movies
        selected_movie = st.selectbox("Select the Movie Name", movies_title)

    st.write("\n" * 2)

    # Display recommendations when the "Recommend" button is clicked
    if st.button("Recommend", key="movie_recommend_button"):
        recommendations = recommend(selected_movie)

        with open("css/showstyles.css", "r") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

        # Initialize watchlist session state if not present
        if "watchlist" not in st.session_state:
            st.session_state["watchlist"] = []


        for index, movie_data in enumerate(recommendations):
            # Create a clickable card for each movie
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    # Display movie poster image, default to a placeholder if not available
                    if movie_data["poster_url"]:
                        st.image(movie_data["poster_url"], width=180)
                    else:
                        st.image("/home/rguktrkvalley/PycharmProjects/movie-recommendation/static/home_banner.png", width=180)

                with col2:
                    # Display movie details such as genre, year, IMDb rating, etc.
                    imdb_url = f"https://www.imdb.com/title/{movie_data['imdb_id']}/"
                    st.markdown(f"""
                            <div class='movie-details'>
                                <div class='title'>{movie_data['title']}</div>
                                <p><strong>Year:</strong> {movie_data['year']}</p>
                                <p><strong>Genre:</strong> {movie_data['genre']}</p>
                                <p><strong>IMDb Rating:</strong> {movie_data['imdb_rating']}</p>
                                <p><strong>IMDb Link:</strong> <a href='{imdb_url}' target='_blank'>View on IMDb</a></p>
                                <div class='movie-plot'>{movie_data['plot']}</div>
                            </div>
                        """, unsafe_allow_html=True)

                    st.button(
                        f"Add to Watchlist - {movie_data['title']}",
                        key=f"add_watchlist_{index}",
                        on_click=add_movie_to_watchlist,
                        args=(movie_data,)
                    )

