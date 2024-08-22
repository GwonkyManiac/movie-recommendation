from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from tmdbv3api import TMDb, Movie
import pandas as pd
from assets import API_KEY, token
import requests
from database import db_connection


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

@app.route('/')
def index():        
        
    genre_dict = fetch_genre_list()
    genre_list = list(genre_dict.values())
    if request.method == 'POST':

        
        #selected_genres = request.form.getlist('genre')  # Get selected genres as a list
        recommendations = get_recommendations()
        return render_template('index.html', recommendations=recommendations, genres= genre_list)
    
    else:
        # Fetch unique genres from the TMDB API
        #selected_genres = request.form.getlist('genre')
        genre_dict = fetch_genre_list()
        genre_list = list(genre_dict.values())
        return render_template('index.html',  genres= genre_list)

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    movie_name = request.form['movie_name']
    search_result = movie.search(movie_name)
    if search_result:
        first_movie_id = search_result[0].id
        recommendations = movie.recommendations(first_movie_id)

        recommendations_list = list(recommendations)

        recommendations_list.sort(key=lambda x: (-x.popularity, -x.vote_average, x.release_date))

        recommendations = recommendations_list[:10]

         # Fetch genre list from TMDB API using the helper function
        genre_dict = fetch_genre_list()

        for recommendation in recommendations:
            recommendation.genre_names = [genre_dict.get(genre_id, 'Unknown') for genre_id in recommendation.genre_ids]       
                
        return render_template('recommendations.html', recommendations=recommendations)
    else:
        flash('No recommendations found for the entered movie.', 'error')
        return redirect(url_for('index'))

@app.route('/rate_movie', methods=['POST'])
def rate_movie():
    title = request.form['title']
    rating = request.form['rating']

    if rating.isdigit() and 0 <= int(rating) <= 10:
        
        # Code to submit the rating can be added here
        rated_movies.loc[len(rated_movies)] = [title, None, None, None, None, int(rating)]
        
        flash(f"Rated movie {title} as {int(rating)}.", 'success')
        return redirect(url_for('index'))
    else:
        flash('Please enter a valid rating between 0 and 10.', 'error')
        return redirect(url_for('index'))
    

@app.route('/rated_movies')
def rated_movies_list():
    return render_template('rated_movies.html', rated_movies=rated_movies)



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



@app.route('/show_reviewer', methods=['POST'])
def show_reviewer():
    db = db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reviewers")  # Select relevant columns

    reviewers = cursor.fetchall()
    db.close()  # Ensure the database connection is closed       
    
    print("Reviewers:", reviewers)
    if not reviewers:
        flash("No reviewers found.")

    return render_template('index.html', reviewers=reviewers)



if __name__ == '__main__':
    app.run(debug=True)
