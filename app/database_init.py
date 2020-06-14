import psycopg2
from services import database

conn = database.connect()

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users(
            id serial PRIMARY KEY,
            name VARCHAR (50) NOT NULL,
            picture VARCHAR (355)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS clothes(
            id serial PRIMARY KEY,
            name VARCHAR (50) NOT NULL,
            email VARCHAR (50) NOT NULL,
            size VARCHAR (3) NOT NULL
        )
        """
    )

    try:
        cur = conn.cursor()
        for c in commands:
            cur.execute(c)
            print("Tables was created successfully!")
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()