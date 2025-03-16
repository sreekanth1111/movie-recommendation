import time
import pandas as pd
import streamlit as st
from auth import get_all_users, add_user, delete_user, update_user
from ui import add_custom_css, signup, login, show_movie_recommendations
from db import create_tables, get_watchlist, remove_from_watchlist

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "role" not in st.session_state:
    st.session_state["role"] = ""
if "view" not in st.session_state:
    st.session_state["view"] = "login"



def homepage():
    st.title("🎬 Movie Recommendation System")
    st.image(
        "/home/rguktrkvalley/PycharmProjects/movie-recommendation/static/index.jpg",
        use_container_width=True,
    )

    # Introductory Section
    st.markdown(
        """
        <div style="background-color:#e3f2fd;padding:15px;border-radius:10px;box-shadow:2px 2px 10px #ddd;color:#333;">
        <strong>Welcome to the future of movie discovery!</strong>  
        With personalized recommendations, a massive database of films, and AI-powered insights, our platform is here to redefine your movie-watching experience.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Benefits Section
    st.header("🌟 Why Choose Us?")
    st.markdown(
        """
        - 🎥 **Tailored Recommendations**: Movies curated just for you based on your unique taste.
        - 💾 **Watchlist Management**: Save and organize movies to watch later.
        - 🧑‍💻 **User-Friendly Interface**: Seamless navigation and visually appealing design.
        - 📊 **Admin Dashboard**: Tools for managing accounts and analyzing data.
        """
    )

    # How It Works Section
    st.header("📖 How It Works")
    st.markdown(
        """
        - **Sign Up or Log In**: Create your account to get started.  
        - **Select a Movie**: Tell us what you've enjoyed watching.  
        - **Get Recommendations**: Discover similar movies instantly.  
        - **Explore Your Watchlist**: Save your favorite picks for later.  
        """
    )


    # User Testimonials Section
    st.header("🎉 What Our Users Say")
    testimonials = [
        "This app is a game-changer! I’ve discovered so many great movies. - Sarah T.",
        "The recommendations are spot-on, and I love the interface! - Jason K.",
        "A must-have for every movie lover. Highly recommend it! - Priya M.",
    ]
    for testimonial in testimonials:
        st.success(testimonial)

    # Call to Action Section
    st.header("🚀 Ready to Discover Your Next Favorite Movie?")
    st.markdown(
        """
        Don't wait! Click the **"Recommend"** button on the sidebar to start your journey.  
        Whether it's a cozy weekend or an exciting movie night, we've got something special for you!
        """
    )
    if st.button("Start Discovering Movies Now"):
        st.balloons()
        time.sleep(2)
        st.session_state["view"] = "movie_recommendations"
        st.rerun()

    # Footer Section
    st.markdown("---")
    st.markdown(
        """
        **About Us**  
        Created by a passionate team of developers, movie buffs, and AI experts.  
        Stay connected with us on [Twitter](https://twitter.com), [Instagram](https://instagram.com), and [LinkedIn](https://linkedin.com).  
        """
    )

def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""
    st.session_state["view"] = "login"
    st.success("You have been logged out. Redirecting to homepage...")
    time.sleep(2)
    st.rerun()




# Admin Dashboard with CRUD operations
def admin_dashboard():
    st.subheader(":bar_chart: Admin Dashboard")
    st.write("---")


    # Display user data
    users = get_all_users()
    if users:
        st.write("### Current Users")
        user_data = pd.DataFrame(users, columns=["ID", "Username", "Password", "Role"])
        user_data.set_index("ID", inplace=True)
        st.table(user_data)

        # Add User Section
        st.write("### Add New User")
        with st.form("add_user_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["Admin", "User"])
            submitted = st.form_submit_button("Add User")
            if submitted:
                add_user(username, password, role)
                st.session_state["view"] = "dashboard"
                st.rerun()

        # Edit User Section
        st.write("### Edit User")
        with st.form("edit_user_form"):
            username = st.text_input("Username", key="username_input")
            new_password = st.text_input("New Password", type="password", key="password_input")
            new_role = st.selectbox("New Role", ["Admin", "User"], key="edit_role")
            if st.form_submit_button("Update User"):
                update_user(username, new_password, new_role)
                st.session_state["view"] = "dashboard"
                st.rerun()

        # Delete User Section
        st.write("### Delete User")
        with st.form("delete_user_form"):
            username = st.text_input("Username",key="delete_user")
            if st.form_submit_button("Delete User"):
                delete_user(username)
                st.session_state["view"] = "dashboard"
                st.rerun()
    else:
        st.write("No users found.")





def display_watchlist(username):
    watchlist = get_watchlist(username)  # Fetch the watchlist from your database
    st.subheader("Your Watchlist")

    if watchlist:
        # Convert watchlist to DataFrame for better handling
        watchlist_df = pd.DataFrame(watchlist, columns=["ID", "Username", "Movie Name", "Poster URL", "Genre", "Year", "IMDb Rating"])
        watchlist_df.set_index("ID", inplace=True)

        # Display the watchlist as an interactive dataframe
        # st.dataframe(watchlist_df[["Movie Name", "Genre", "Year", "IMDb Rating"]])

        # Display each movie with its poster and details
        for idx, row in watchlist_df.iterrows():
            st.markdown(f"**{row['Movie Name']}**")
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(row['Poster URL'], width=100)
            with cols[1]:
                st.markdown(f"**Genre:** {row['Genre']}")
                st.markdown(f"**Year:** {row['Year']}")
                st.markdown(f"**IMDb Rating:** {row['IMDb Rating']}")

            # Button to remove the movie from the watchlist
            if st.button(f"Remove from Watchlist", key=f"remove_{idx}"):
                remove_from_watchlist(username, row['Movie Name'])
                st.success(f"Removed {row['Movie Name']} from your watchlist.")
                st.rerun()  # Refresh the watchlist display
    else:
        st.write("Your watchlist is empty.")



def main():
    add_custom_css()
    create_tables()

    st.sidebar.title("🧭 Navigation")
    if st.session_state.get("logged_in", False):
        st.sidebar.write(f"Logged in as: **{st.session_state['username']}** ({st.session_state['role']})")

        if st.sidebar.button("Home", key="homepage_button"):
            st.session_state["view"] = "homepage"
            st.rerun()

        if st.sidebar.button("Recommend", key="movie_recommendations_button"):
            st.session_state["view"] = "movie_recommendations"
            st.rerun()

        if st.sidebar.button("Watchlist", key="watchlist_button"):
            st.session_state["view"] = "watchlist"
            st.rerun()

        if st.session_state['role'] == 'Admin':
            if st.sidebar.button("Dashboard", key="dashboard_button"):
                st.session_state["view"] = "dashboard"
                st.rerun()

        if st.sidebar.button("Logout", key="logout_button"):
            logout()

        # Display views based on session state
        if st.session_state["view"] == "homepage":
            homepage()
        elif st.session_state["view"] == "dashboard":
            admin_dashboard()
        elif st.session_state["view"] == "movie_recommendations":
            show_movie_recommendations()
        elif st.session_state["view"] == "watchlist":
            display_watchlist(st.session_state["username"])

    else:
        st.sidebar.button("Login", key="go_to_login", on_click=lambda: st.session_state.update(view="login"))
        st.sidebar.button("Sign Up", key="go_to_signup", on_click=lambda: st.session_state.update(view="signup"))

        if st.session_state["view"] == "login":
            login()
        elif st.session_state["view"] == "signup":
            signup()


if __name__ == "__main__":
    main()
