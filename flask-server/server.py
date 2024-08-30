
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from database import db_connection
from flask_cors import CORS
from tmdbv3api import TMDb, Movie
from asset import API_KEY, token
import requests
from database import db_connection


app = Flask(__name__)
app.secret_key = token
tmdb = TMDb()
tmdb.api_key = API_KEY
movie = Movie()
CORS(app)

#rated_movies = pd.DataFrame(columns=["title", "release_date", "popularity", "genre_ids", "vote_average", "rating"])
#@app.route('/', methods=["GET"])
def fetch_genre_list():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    headers = {
        "accept": "application/json",        
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        genre_list = response.json()['genres']
        genre_dict = {genre['id']: genre['name'] for genre in genre_list}       
        
        return genre_dict
    else:
        return None

@app.route('/genres', methods=["GET"])
def get_genres():
    genre_dict = fetch_genre_list()
    genre_list = list(genre_dict.values())
    
    return jsonify(genre_list)

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    movie_name = data['movie_name']
    search_result = movie.search(movie_name)
    
    if search_result:
        first_movie_id = search_result[0].id
        recommendations = movie.recommendations(first_movie_id)

        recommendations_list = list(recommendations)
        recommendations_list.sort(key=lambda x: (-x.popularity, -x.vote_average, x.release_date))
        recommendations = recommendations_list[:10]

        genre_dict = fetch_genre_list()

        for recommendation in recommendations:
            recommendation.genre_names = [genre_dict.get(genre_id, 'Unknown') for genre_id in recommendation.genre_ids]     
            
        return jsonify([{
            'title': req.title,
            'release_date': req.release_date,
            'popularity': req.popularity,
            'genre_names': req.genre_names,
            'vote_average': req.vote_average
        } for req in recommendations])
    else:
        return jsonify({"error": "no recommendation found"}) , 404
            

@app.route('/add_reviewer', methods=['POST'])
def add_reviewer():
    db = db_connection()
    cursor = db.cursor()
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    cursor.execute("INSERT INTO reviewers (first_name, last_name) VALUES (%s, %s)", (first_name, last_name))
    db.commit()
    flash(f'Reviewer {first_name} {last_name} added successfully!', 'success')
    return redirect(url_for('index'))



@app.route('/show_reviewer', methods=['GET'])
def show_reviewer():
    db = db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reviewers")
    reviewers = cursor.fetchall()
    reviewers_list = [{"First name ": row[0], "Last name": row[1]} for row in reviewers]
    return jsonify(reviewers_list) 

@app.route('/rate_movie', methods=['POST'])
def show_ratings():
    
    data = request.json
    rating = data['rating']
    movie_id = data['movie_id']
    reviewer_id = data['reviewer_id']
    
    
    db = db_connection()
    cursor = db.cursor()   
    cursor.execute("INSERT INTO ratings (rating, movie_id, reviewer_id) VALUES ( %s, %s, %s)",(rating, movie_id, reviewer_id ))
    db.commit()
        
        #return redirect(url_for('rate_movie'))
    return jsonify({"message": "Rating added successfully!"}), 200
    


if __name__ == '__main__':
    app.run(debug=True, port=5000)