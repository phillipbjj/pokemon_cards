import os
from dotenv import load_dotenv
import psycopg2
from datetime import date

load_dotenv()
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password=os.getenv('PHILPW'),
        host="localhost",
        port="1007",
        )
    print("Database connection successful")

    cur = conn.cursor()

    cur.execute('''INSERT INTO users (username, password, email) 
                VALUES (%s, %s, %s)''', 
                (username, password, email)
                )
    conn.commit()

except Exception as e:
    print(f"An error occurred: {e}")
    print("F homie")