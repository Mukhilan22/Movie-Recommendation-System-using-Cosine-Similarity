import numpy as np
import streamlit as st
import pandas as pd
import difflib
import requests

# MOVIES AND COSINE SIMILARITY ARRAY
similarity = np.load('similarity.npy')
movies = np.load('movies.npy', allow_pickle=True)

# TO FETCH MOVIE POSTERS USING OMDB API
API_KEY = '3addd193'
API_URL = 'http://www.omdbapi.com/'

st.markdown("<h1 style='text-align: center;'> MUKHI's MOVIE RECOMMENDER </h1>", unsafe_allow_html=True)
movie_name = st.text_input("ENTER MOVIE NAME :film_projector:")
movie_name = movie_name.lower()

def fetch_poster(movie):
    search_url = f"{API_URL}?apikey={API_KEY}&t={movie}"
    response = requests.get(search_url)
    data = response.json()
    
    if data['Response'] == 'True':
        poster_url = data.get('Poster')
        return poster_url
    return None

def recommend(movie_name,movies,similarity):

    find_close_match=difflib.get_close_matches(movie_name, movies) # Gives 3 Names from movie names closest to our input
    close_match = find_close_match[0]

    index = np.where(close_match==movies)[0][0] 
    req = (similarity[index])
    row = list(enumerate(req))

    row.sort(key = lambda x: x[1], reverse=True)
    recommends=row[1:13]

    results=[movies[i] for i,score in recommends]
    posters = [fetch_poster(x) for x in results]

    return results, posters

st.write(""" #### RECOMMENATIONS: """)
if movie_name:
    
    result, posters = recommend(movie_name,movies,similarity)


    # Create columns for layout
    num_columns = 4
    columns = st.columns(num_columns)

    for i in range(0, len(result), num_columns):   # Iterates over the result list in chunks of size num_columns.
                end = min(i + num_columns, len(result)) # Determines the endpoint of the current chunk of items
                for j in range(i, end): # Iterates over the indices of the current chunk of items from i to end
                    col = columns[j % num_columns] # Selects the appropriate column from the columns list for displaying the current item.
                    with col:
                        poster_url = posters[j]
                        if poster_url:
                            st.image(poster_url, caption=result[j], use_column_width=True)
                        else:
                            st.write(poster_url)
                            st.write(result[j])  # If poster URL is not found
