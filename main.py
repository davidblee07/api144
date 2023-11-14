from flask import Flask, jsonify, request
from demographic_filtering import output
from content_filtering import get_recommendations
import pandas as pd

movies_data = pd.read_csv('final.csv')

app = Flask(__name__)

all_movies = movies_data[["original_title","poster_link","release_date","runtime","weighted_rating"]]

liked_movies = []
not_liked_movies = []
did_not_watch = []

def assign_val():
    m_data = {
        "original_title": all_movies.iloc[0,0],
        "poster_link": all_movies.iloc[0,1],
        "release_date": all_movies.iloc[0,2] or "N/A",
        "duration": all_movies.iloc[0,3],
        "rating":all_movies.iloc[0,4]/2
    }
    return m_data

@app.route("/movies")
def get_movie():
    movie_data = assign_val()

    return jsonify({
        "data": movie_data,
        "status": "success"
    })

@app.route("/like")
def liked_movie():
    global all_movies
    movie_data=assign_val()
    liked_movies.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies = all_movies.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

# api para retornar a lista de filmes curtidos
@app.route('/liked')
def liked():
    global liked_movies
    return jsonify({
        'data': liked_movies,
        'status':'success'
    })



@app.route("/dislike")
def unliked_movie():
    global all_movies

    movie_data=assign_val()
    not_liked_movies.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    
    return jsonify({
        "status": "success"
    })

@app.route("/did_not_watch")
def did_not_watch_view():
    global all_movies

    movie_data=assign_val()
    did_not_watch.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    
    return jsonify({
        "status": "success"
    })

# api para retornar a lista de filmes populares
@app.route('/popular_movies')
def popular_movies():
    popular_movie_data = []
    for index, row in output.iterrows():
        p = {
        "original_title": row['original_title'],
        "poster_link": row['poster_link'],
        "release_date": row['release_date'] or "N/A",
        "duration": row['runtime'],
        "rating":row['weighted_rating']
        }
        popular_movie_data.append(p)
    return jsonify({
        'data': popular_movie_data,
        'status':'success'
    })    


# api para retornar a lista de filmes recomendados
@app.route('/recommended_movies')
def recommended_movies():
    global liked_movies
    columns_names = ["original_title","poster_link","release_date","runtime","weighted_rating"]
    all_recommended = pd.DataFrame(columns = columns_names)
    for liked_movie in liked_movies:
        output = get_recommendations(liked_movie['original_title'])
        all_recommended = pd.concat([all_recommended, output], axis = 0)
    all_recommended.drop_duplicates(subset = ['original_title'], inplace = True)
    recommended_movie_data = []
    for index, row in all_recommended.iterrows():
        p = {
        "original_title": row['original_title'],
        "poster_link": row['poster_link'],
        "release_date": row['release_date'] or "N/A",
        "duration": row['runtime'],
        "rating":row['weighted_rating']
        }
        recommended_movie_data.append(p)   
    return jsonify({
        'data': recommended_movie_data,
        'status': 'success'
    })      


if __name__ == "__main__":
  app.run()
