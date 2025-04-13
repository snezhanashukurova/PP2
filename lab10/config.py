import psycopg2

def connect_to_db():
    return psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='12345678'  
    )
