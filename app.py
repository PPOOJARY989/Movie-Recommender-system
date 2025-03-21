
import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

url = "https://api.themoviedb.org/3/movie/35?language=en-US"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0YTc3MDE4ZDU4ZGZlNDdmMDFhZTAyNjNkYmRiZDdkMCIsIm5iZiI6MTcyMDI3OTU2OC42NDYwMjUsInN1YiI6IjY2ODk2MDlhMzcyMDg3MTNhYTg5MDcxMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.YjVe-WO5x8ngdrRAivUyajM-FuJbL_7AS8y30PGqSsU"
}

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id), headers=headers)
    data = response.json()
    if 'poster_path' in data and data['poster_path'] is not None:
        return "https://image.tmdb.org/t/p/w185/" + data['poster_path']
    else:
        return "https://via.placeholder.com/185x278?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Enter the name of the movie',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
