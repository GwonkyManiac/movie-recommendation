from mysql.connector import connect, Error
from asset import DB_USERNAME, DB_PASSW
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