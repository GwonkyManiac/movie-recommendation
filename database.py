from getpass import getpass
from mysql.connector import connect, Error
from assets import DB_USERNAME, DB_PASSW
import mysql


def db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user=DB_USERNAME,
            passwd=DB_PASSW,
            auth_plugin='mysql_native_password',
            database= "movie_rating_app"
        )
        if db.is_connected():
            print("Connected to MySQL database")
            return db
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

   
 #create datatables. maybe not useful to have in code since only run ones. so might remove later           
def create_review_table(db):
    review_table_query = "CREATE TABLE reviewers (first_name VARCHAR(100) NOT NULL, last_name VARCHAR(100), id INT(11) PRIMARY KEY AUTO_INCREMENT)"    
    db.cursor().execute(review_table_query)
    db.commit()
    
            
def create_rating_table(db):
    rating_table_query = "CREATE TABLE ratings (movie_id INT(11) NOT NULL, reviewer_id INT(11) NOT NULL, rating DECIMAL(2,1) NOT NULL, FOREIGN KEY(reviewer_id) REFERENCES reviewers(id), FOREIGN KEY(movie_id) REFERENCES movies(id), PRIMARY KEY(movie_id, reviewer_id))"
    db.cursor().execute(rating_table_query)
    db.commit()

            
def create_movie_table(db):
    movie_table_query = "CREATE TABLE movies (title VARCHAR(100) NOT NULL, release_year YEAR(4), popularity INT(11) NOT NULL , genre VARCHAR(100), collection_in_mil DECIMAL(4,1), id INT(11) PRIMARY KEY AUTO_INCREMENT)"
    cursor =  db.cursor()
    cursor.execute(movie_table_query)
    db.commit()
    
    
#create a reviwer. will be a button that asks for name and last name
# maybe already here add preferences on movies they like: genres, only top movies ( popularity), length? release date  

def  create_reviwer(cursor, first_name, last_name):
    cursor.execute("INSERT INTO reviewers (first_name , last_name) VALUES (%s,%s)", (first_name, last_name))
    db.commit()
    cursor.execute("SELECT * FROM reviewers")  
    for x in cursor:
        print(x)
        
#define movies. They already fetch from an api tmdbi so this step might be removed. 
def  create_movies(cursor, title, release_year,popularity,genre,collection_in_mil):
    cursor.execute("INSERT INTO ratings (title , release_year, popularity, genre, collection_in_mil) VALUES (%s,%s,%s,%s%s)", (title, release_year,popularity,genre,collection_in_mil))
    db.commit()
    cursor.execute("SELECT * FROM movies")  
    for x in cursor:
        print(x)
        
def  rate_movie(cursor, title, release_year,popularity,genre,collection_in_mil):
    cursor.execute("INSERT INTO ratings (movie_id , reviewer_id, rating, genre, collection_in_mil) VALUES (%s,%s,%s,%s%s)", (title, release_year,popularity,genre,collection_in_mil))
    db.commit()
    cursor.execute("SELECT * FROM ratings")  
    for x in cursor:
        print(x)
        
        
 
 #movie_id INT(11) NOT NULL, reviewer_id INT(11) NOT NULL, rating DECIMAL(2,1) NOT NULL, FOREIGN KEY(reviewer_id) REFERENCES reviewers(id), FOREIGN KEY(movie_id) REFERENCES movies(id), PRIMARY KEY(movie_id, reviewer_id    
#rate movie coupled to a reviwer. might add a list so we can review alot of movies at the same time  
     
#create_reviwer(mycursor, "Bella", "Hansen")
#mycursor.execute("INSERT INTO Person (name , age) VALUES (%s,%s)", ("Gustav", 28))
def update_rating(db, new_rating,    movie_id,         reviewer_id):
    update_query = """
    UPDATE
        ratings
    SET
        rating = %s
    WHERE
        movie_id = %s AND reviewer_id = %s;

    SELECT *
    FROM ratings
    WHERE
        movie_id = %s AND reviewer_id = %s
    """ 
    val_tuple =  (
        new_rating,
        movie_id,
        reviewer_id,
        movie_id,
        reviewer_id
    )
    db.cursor.execute(update_query, val_tuple, multi=True)
    db.commit()
    
    
def show_revewer(cursor):    
    cursor.execute("SELECT * FROM ratings")  
    for x in cursor:
        print(x)
    

# Example usage
if __name__ == "__main__":
    db = db_connection()
    if db:
        create_cursor = db.cursor(buffered=True)        
        #create_review_table(db)
        #create_rating_table(db)
        db.close()

#

