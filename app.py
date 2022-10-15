import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(mov_id):
    res = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(mov_id))
    data = res.json()

    return "https://image.tmdb.org/t/p/w342" + data['poster_path']


def recommend(movie):
    sim_list = list(enumerate(sim[ismovies[movie]]))
    sim_list = sorted(sim_list, key=lambda x: x[1], reverse=True)
    sim_list = sim_list[1:11]

    movs = []
    movs_poster = []
    #movs_overview = []

    for i in sim_list:
        mov_id = movies.iloc[i[0]]
        movs.append(mov_id.title)
        movs_poster.append(fetch_poster(mov_id.id))
    #   movs_overview.append(mov_id.overview)

    return movs, movs_poster  # , movs_overview


def improved_recommend(movie):
    sim_list = list(enumerate(sim[ismovies[movie]]))
    sim_list = sorted(sim_list, key=lambda x: x[1], reverse=True)
    sim_list = sim_list[1:21]

    movs = pd.DataFrame
    rec_movs = []
    movs_poster = []
    #movs_overview = []

    sim_movies = [i[0] for i in sim_list]
    movs = movies.iloc[sim_movies][[
        'title', 'vote_count', 'vote_average', 'id']]

    vote_counts = movs[movs['vote_count'].notnull()
                       ]['vote_count'].astype('int')
    vote_averages = movs[movs['vote_average'].notnull()
                         ]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(0.20)

    # Creating df of movies having vote count above the 'm'
    qualified = movs[(movs['vote_count'] >= m) & (
        movs['vote_count'].notnull()) & (movs['vote_average'].notnull())]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')

    # (v / ( v + m ) * R) + ( m / ( m + v ) * C) -> v = vote count R = vote avg C = avg mean m = Minimum votes req
    qualified['Score'] = qualified.apply(lambda x: (
        x['vote_count']/(x['vote_count']+m) * x['vote_average']) + (m/(m+x['vote_count']) * C), axis=1)

    qualified = qualified.sort_values('Score', ascending=False).head(10)

    for i in range(qualified.shape[0]):
        rec_movs.append(qualified.iloc[i][['title']][0])
        movs_poster.append(fetch_poster(qualified.iloc[i][['id']][0]))
    #   movs_overview.append(i.overview)

    return rec_movs, movs_poster  # , movs_overview


sim = pickle.load(open('sim.pkl', 'rb'))
ismovies = pickle.load(open('ismovies.pkl', 'rb'))
movies = pickle.load(open('smovies.pkl', 'rb'))
movies = pd.DataFrame(movies)

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    'Please enter your favorite movie', movies['title'].values)

val = st.checkbox('Imporved Recommendetion', value=False,
                  help='Recommendetion will be further filtered by ratings and will be sorted')

if st.button('Recommend'):
    st.header('You might also like these movies...')
    j = 0
    if val:
        recs, recs_poster = improved_recommend(selected_movie)
    else:
        recs, recs_poster = recommend(selected_movie)
    for i in range(2):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(recs_poster[j])
            st.write(recs[j])
            # st.write(recs_overv[j])
            j = j+1
        with col2:
            st.image(recs_poster[j])
            st.write(recs[j])
            # st.write(recs_overv[j])
            j = j+1
        with col3:
            st.image(recs_poster[j])
            st.write(recs[j])
            # st.write(recs_overv[j])
            j = j+1
        with col4:
            st.image(recs_poster[j])
            st.write(recs[j])
            # st.write(recs_overv[j])
            j = j+1
        with col5:
            st.image(recs_poster[j])
            st.write(recs[j])
            # st.write(recs_overv[j])
            j = j+1
