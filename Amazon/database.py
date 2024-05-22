import psycopg2

def connect_db():
    return psycopg2.connect(
        dbname="flaskdb",
        user="postgres",
        password="sfdc",
        host="localhost",
        port="5432"
    )

def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS laptop_list (
            title TEXT PRIMARY KEY,
            star TEXT,
            price TEXT
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def store_laptop(laptop):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO laptop_list (title, star, price)
        VALUES (%s, %s, %s)
    ''', (laptop['title'], laptop['star'], laptop['price']))
    conn.commit()
    cur.close()
    conn.close()

create_table()