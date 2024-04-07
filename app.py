# Importing necessary libraries
import pickle
import streamlit as st
import requests
from PIL import Image

# Function to fetch the movie poster from TMDB API using the movie ID
def fetch_poster(movie_id):
    # Constructing the URL with the given movie ID and API key
    url=f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d9664b9b9983b0798c6131bc8d9427e0'
    # Making the request to the URL
    data=requests.get(url).json()  # Parsing the response to JSON
    poster_path=data['poster_path']  # Extracting the poster path
    full_path="https://image.tmdb.org/t/p/w500/" + poster_path  # Constructing the full URL for the poster
    return full_path  # Returning the full poster URL

# Function to recommend movies based on a given movie name
def recommend(movie_name):
    recommended_movie_names = []  # List to store the recommended movie names
    recommended_movie_poster = []  # List to store the URLs of the recommended movie posters
    # Finding the index of the given movie name in the dataframe
    index = movies[movies['title'] == movie_name].index[0]
    # Calculating similarity scores and sorting them in descending order
    similarity = sorted(list(enumerate(similari[index])), reverse=True, key=lambda x: x[1])[0:10]
    for i, _ in similarity:
        # For each recommended movie, fetching its poster and title
        url = fetch_poster(movies.loc[i, "movie_id"])
        title = movies.loc[i, "title"]
        recommended_movie_names.append(title)  # Adding the title to the list
        recommended_movie_poster.append(url)  # Adding the poster URL to the list
    return recommended_movie_names, recommended_movie_poster  # Returning the lists

# Loading the movie dataset and similarity matrix from pickle files
movies = pickle.load(open("final_df.pkl", "rb"))
similari = pickle.load(open("similarity.pkl", "rb"))

# Loading and displaying an image banner for the app
image = Image.open("recom.jpg")
st.image(image, width=120)

# Setting up the Streamlit app header
st.header("Film Recommendation System")

# Creating a selection box with all movie titles
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Input the name of a movie or choose one from the provided list",
    movie_list
)

# Button to trigger the recommendation process
if st.button('Display The Recommendations'):
    # Getting recommendations for the selected movie
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    # Displaying the recommended movies and their posters in a 5x2 grid
    for i in range(0, 10, 5):
        cols = st.columns(5)
        for j in range(5):
            with cols[j]:
                st.image(recommended_movie_posters[i+j])
                st.caption(recommended_movie_names[i+j])