from configparser import ConfigParser
import psycopg2


def config(filename='src/database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {} not found in the {} file'.format(section, filename))
    return db


def connect():
    conn = None
    try:
        params = config()

        print("Connectiong to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute("""
        CREATE TABLE vectors (
            size INTEGER NOT NULL,
            vector1 VARCHAR(10) NOT NULL,
            vector2 VARCHAR(10) NOT NULL,
            vector3 VARCHAR(10) NOT NULL,
            vector4 VARCHAR(10) NOT NULL,
            vector5 VARCHAR(10) NOT NULL,
            vector6 VARCHAR(10) NOT NULL,
            vector7 VARCHAR(10) NOT NULL,
            vector8 VARCHAR(10) NOT NULL,
            vector9 VARCHAR(10) NOT NULL,
            vector11 VARCHAR(10) NOT NULL,
            vector12 VARCHAR(10) NOT NULL,
            vector13 VARCHAR(10) NOT NULL,
            vector14 VARCHAR(10) NOT NULL,
            vector15 VARCHAR(10) NOT NULL,
            vector16 VARCHAR(10) NOT NULL,
            vector17 VARCHAR(10) NOT NULL,
            vector18 VARCHAR(10) NOT NULL,
            vector19 VARCHAR(10) NOT NULL,
            vector20 VARCHAR(10) NOT NULL,
            vector21 VARCHAR(10) NOT NULL
            )""")

        db_version = cur.fetchone()
        print(db_version)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
