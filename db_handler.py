import psycopg2
from psycopg2 import sql

def create_table():

    conn = psycopg2.connect(
       dbname="flaskdb",
       user="postgres",
       password="sfdc",
       host="localhost",
       port="5432"
    )
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS laptops (
            title TEXT PRIMARY KEY,
            stars TEXT,
            current_price TEXT,
            previous_price TEXT
        )
    ''')
    conn.commit()
    c.close()
    conn.close()


def store_laptops(laptops):

    conn = psycopg2.connect(
        dbname="flaskdb",
        user="postgres",
        password="sfdc",
        host="localhost",
        port="5432"
    )
    c = conn.cursor()

    for laptop in laptops:
        c.execute('''
            INSERT INTO laptops (title, stars, current_price, previous_price)
            VALUES (%s, %s, %s, %s)
        ''', (laptop['Title'], laptop['Stars'], laptop['Current Price'], laptop['Previous Price']))

    conn.commit()
    c.close()
    conn.close()


# Ensure the table is created when the module is imported
create_table()
