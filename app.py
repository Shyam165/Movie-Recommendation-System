import pickle
import streamlit as st
import requests
import pandas as pd
from PIL import Image
import bz2file as bz2

# Set a background image or color
# st.markdown('<style>div[class="css-zbg2rx e1fqkh3o1"] {color:black; background: url("mv.png");background-repeat: no-repeat;background-size:350%;} </style>', unsafe_allow_html=True)

# Title and description
st.title('Movie Recommendation System')
st.write('Discover movies similar to your favorites!')

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names,recommended_movie_posters


# Header image or logo
header_image = Image.open('movies_logo.jpeg')
header_image_resized = header_image.resize((600, 100))  # Adjust the size as needed
st.image(header_image_resized, caption='Movie Recommender')

def decompress_pickle(file):
    with bz2.BZ2File(file, 'rb') as data:
        data = pickle.load(data)
    return data

movies_dict = decompress_pickle('movie_dict.pbz2')
similarity = decompress_pickle('similarity.pbz2')

# movies_dict = pickle.load(open('movie_dict.sav','rb'))
movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.sav','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    st.write('Recommended Movies:')
    cols = st.columns(5)
    with cols[0]:
      st.text(recommended_movie_names[0])
      st.image(recommended_movie_posters[0])
    with cols[1]:
      st.text(recommended_movie_names[1])
      st.image(recommended_movie_posters[1])
    with cols[2]:
      st.text(recommended_movie_names[2])
      st.image(recommended_movie_posters[2])
    with cols[3]:
      st.text(recommended_movie_names[3])
      st.image(recommended_movie_posters[3])
    with cols[4]:
      st.text(recommended_movie_names[4])
      st.image(recommended_movie_posters[4])

# Footer or contact information
st.write('For feedback or inquiries, contact us at: email@gmail.com')