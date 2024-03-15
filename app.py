
import streamlit as st


st.markdown(
        f"""
        <style>
            {open("styles.css").read()}
        </style>
        """,
        unsafe_allow_html=True
    )
st.title('Movie Recommender')
import requests
import pandas as pd
import pickle



with open('movies.pkl','rb') as file:
    movies_df=pd.read_pickle(file)
#movies_df=pickle.load(open('movies.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
m_l=movies_df['title'].values

selected_movie = st.selectbox(
    'Choose any below listed movie',
   (m_l))

def fetch_poster(movie_id):
    
    url = "https://api.themoviedb.org/3/movie/{}?api_key=bbb8f24c1d1fa8ab724e640749026cb5&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
   

def recommendations(movie):
    movie_index=movies_df[movies_df['title']==movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(enumerate(distances),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movie_list:        
        recommended_movies.append(movies_df.iloc[i[0]].title)
        poster=fetch_poster(movies_df.iloc[i[0]].id)
        recommended_movies_posters.append(poster)
    return recommended_movies,recommended_movies_posters    

if st.button('Recommend'):    
   recommended_movies,posters=recommendations(selected_movie)
   col1, col2, col3, col4, col5 = st.columns(5)
   with col1:
       st.text(recommended_movies[0])
       st.image(posters[0])
   with col2:
       st.text(recommended_movies[1])
       st.image(posters[1])
   with col3:
       st.text(recommended_movies[2])
       st.image(posters[2])
   with col4:
       st.text(recommended_movies[3])
       st.image(posters[3])
   with col5:
       st.text(recommended_movies[4])
       st.image(posters[4])      
       
