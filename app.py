from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from tmdbv3api import TMDb, Movie
import pandas as pd
from assets import API_KEY, token
import requests

app = Flask(__name__)
app.secret_key = token
tmdb = TMDb()
tmdb.api_key = API_KEY
movie = Movie()

rated_movies = pd.DataFrame(columns=["title", "release_date", "popularity", "genre_ids", "vote_average", "rating"])

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

@app.route('/', methods=['GET', 'POST'])
def index():
    genre_dict = fetch_genre_list()
    genre_list = list(genre_dict.values())
    if request.method == 'POST':
        recommendations = get_recommendations()
        return render_template('index.html', recommendations=recommendations, genres=genre_list)
    else:
        return render_template('index.html', genres=genre_list)

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    selected_genres = request.form.getlist('genres[]')
    movie_name = request.form['movie_name']
    search_result = movie.search(movie_name)
    
    # Print the selected genres for debugging
    print("Selected genres:", selected_genres)
    
    if search_result:
        first_movie_id = search_result[0].id
        recommendations = movie.recommendations(first_movie_id)

        recommendations_list = list(recommendations)

        recommendations_list.sort(key=lambda x: (-x.popularity, -x.vote_average, x.release_date))

        recommendations = recommendations_list[:15]
        
        genre_dict = fetch_genre_list()
        
        # Filter movies based on selected genres
        if selected_genres:
            filtered_movies = [
                rec for rec in recommendations
                if any(genre_dict.get(genre_id) in selected_genres for genre_id in rec.genre_ids)
            ]
        else:
            filtered_movies = recommendations
        
        for recommendation in filtered_movies:
            recommendation.genre_names = [genre_dict.get(genre_id, 'Unknown') for genre_id in recommendation.genre_ids]
                
        return render_template('recommendations.html', recommendations=filtered_movies)
    else:
        flash('No recommendations found for the entered movie.', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
