from fastapi import FastAPI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

app = FastAPI()

steam_games = pd.read_csv('../data/steam_games.csv')
users_items = pd.read_csv('../data/users_items.csv')
users_reviews = pd.read_csv('../data/users_reviews.csv')

users_reviews['posted_year'] = users_reviews['posted_year'].astype(int)
steam_games['item_id'] = steam_games['item_id'].astype(int)
users_reviews['item_id'] = users_reviews['item_id'].astype(int)

muestra_steam_games = steam_games.head(42000)
muestra_users_items = users_items.head(42000)
muestra_users_reviews = users_reviews.head(42000)

@app.get('/user_for_genre/')
def user_for_genre(genero: str):

   
    juegos_genero = muestra_steam_games[muestra_steam_games['genres'] == genero]

    if juegos_genero.empty:
        return {'message': f'No se encontraron juegos para el género: {genero}'}

    datos_genero = pd.merge(juegos_genero, muestra_users_items, on=['item_id'])

    if datos_genero.empty:
        return {'message': f'No se encontraron datos para el género: {genero}'}

    horas_por_usuario = datos_genero.groupby('user_id')['playtime_forever'].sum()

    usuario_max_horas = horas_por_usuario.idxmax()
    horas_max = horas_por_usuario.max()

    return {
        "Usuario con más horas jugadas en " + str(genero): usuario_max_horas,
        "Horas jugadas por el usuario": int(horas_max)
    }

@app.get('/users_recommend/')
def users_recommend(year: int):

    recommendations = muestra_users_reviews[
        (muestra_users_reviews['recommend'] == True) &
        ((muestra_users_reviews['sentiment_analysis'] == 1) | (muestra_users_reviews['sentiment_analysis'] == 2)) &
        (muestra_users_reviews['posted_year'] == year)
    ]

    if recommendations.empty:
        return {'message': f'No se encontraron recomendaciones para el año: {year}'}

    complete_data = pd.merge(recommendations, muestra_steam_games, on=['item_id'])

    if complete_data.empty:
        return {'message': f'No se encontraron datos de juegos para las recomendaciones del año: {year}'}

    top_3_games = complete_data['item_name'].value_counts().head(3).index.tolist()

    response = [{"Puesto 1": top_3_games[0]}, {"Puesto 2": top_3_games[1]}, {"Puesto 3": top_3_games[2]}]

    return response

@app.get('/users_not_recommend/')
def users_not_recommend(anio: int):

    no_recomendaciones = muestra_users_reviews[(muestra_users_reviews['recommend'] == False) & (muestra_users_reviews['sentiment_analysis'] == 0) & (muestra_users_reviews['posted_year'] == anio)]

    if no_recomendaciones.empty:
        return {'message': f'No se encontraron recomendaciones negativas para el año: {anio}'}

    datos_completos = pd.merge(no_recomendaciones, muestra_steam_games, on=['item_id'])

    if datos_completos.empty:
        return {'message': f'No se encontraron datos de juegos para las recomendaciones negativas del año: {anio}'}

    top_3_juegos = datos_completos['item_name'].value_counts().head(3).index.tolist()

    respuesta = [{"Puesto 1": top_3_juegos[0]}, {"Puesto 2": top_3_juegos[1]}, {"Puesto 3": top_3_juegos[2]}]

    return respuesta

@app.get('/play_time_genre/')
def play_time_genre(genre: str):
   
    genre_games = muestra_steam_games[muestra_steam_games['genres'] == genre]

    if genre_games.empty:
        return {'message': f'No se encontraron juegos para el género: {genre}'}

    merged_data = pd.merge(genre_games, muestra_users_items, on=['item_id'])

    hours_by_year = merged_data.groupby('release_year')['playtime_forever'].sum()

    year_max_hours = hours_by_year.idxmax()

    return {"Año de lanzamiento con más horas jugadas para género " + genre: int(year_max_hours)}

@app.get('/sentiment_analysis/')
def sentiment_analysis(year: int):
   
    reviews_by_year = muestra_users_reviews[muestra_users_reviews['posted_year'] == year]

    if reviews_by_year.empty:
        return {'message': f'No se encontraron reseñas para el año: {year}'}

    sentiment_counts = reviews_by_year['sentiment_analysis'].value_counts().to_dict()

    return {
        "Negative": sentiment_counts.get(0, 0),
        "Neutral": sentiment_counts.get(1, 0),
        "Positive": sentiment_counts.get(2, 0)
    }

muestra_steam_games_modelo = steam_games.head(6000)
muestra_users_reviews_modelo = users_reviews.head(6000)

@app.get('/recomendacion_juego/')
def recommend_game(game_id: int, top_n: int = 5):
    tfidf_vectorizer = TfidfVectorizer()

    tfidf_matrix = tfidf_vectorizer.fit_transform(muestra_steam_games_modelo['genres'])

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    idx = muestra_steam_games_modelo.index[muestra_steam_games_modelo['item_id'] == game_id].tolist()

    recommended_indices = []
   
    if idx:
        idx = idx[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) 
        top_n = int(top_n)
        recommended_indices = [i[0] for i in sim_scores[1:top_n + 1]]

    return list(muestra_steam_games_modelo['item_name'].iloc[recommended_indices])

@app.get('/recomendacion_usuario/')
def recommend_user(id: str):
    user_reviews = muestra_users_reviews_modelo[muestra_users_reviews_modelo['user_id'] == id]
    user_reviews.reset_index(drop=True, inplace=True)

    if not user_reviews.empty:
        game_id = user_reviews['item_id'].iloc[0]  
        recommended_games = recommend_game(game_id=int(game_id))
        return recommended_games
    else:
        return []

@app.get("/")
def index():
    return "Hola amigos!"