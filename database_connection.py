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
        # cur.execute("SET search_path TO {}".format(schema))

        insert_query = """
        CREATE TABLE cuenca.vectors (
        size INTEGER NOT NULL,
        vector1 VARCHAR(10) NULL,
        vector2 VARCHAR(10) NULL,
        vector3 VARCHAR(10) NULL,
        vector4 VARCHAR(10) NULL,
        vector5 VARCHAR(10) NULL,
        vector6 VARCHAR(10) NULL,
        vector7 VARCHAR(10) NULL,
        vector8 VARCHAR(10) NULL,
        vector9 VARCHAR(10) NULL,
        vector11 VARCHAR(10) NULL,
        vector12 VARCHAR(10) NULL,
        vector13 VARCHAR(10) NULL,
        vector14 VARCHAR(10) NULL,
        vector15 VARCHAR(10) NULL,
        vector16 VARCHAR(10) NULL,
        vector17 VARCHAR(10) NULL,
        vector18 VARCHAR(10) NULL,
        vector19 VARCHAR(10) NULL,
        vector20 VARCHAR(10) NULL,
        vector21 VARCHAR(10) NULL
        )"""

        print('PostgreSQL database version:')
        # cur.execute('create schema cuenca')
        # cur.execute('select * from pg_catalog.pg_user')
        cur.execute("SELECT distinct schemaname FROM pg_catalog.pg_tables")
        # cur.execute("show search_path")
        # cur.execute(insert_query)
        db_version = cur.fetchall()
        for row in db_version:
            print(row)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
