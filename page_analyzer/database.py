import psycopg2
from psycopg2.extras import RealDictCursor

from page_analyzer.cfg import DATABASE_URL


def make_db_connection():
    return psycopg2.connect(DATABASE_URL)


def insert_url(url_data):
    query = '''
        INSERT
        INTO urls (name, created_at)
        VALUES (%s, %s)
        RETURNING id
        '''
    with make_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (url_data['url'],
                                   url_data['created_at']))
            return cursor.fetchone()[0]


def get_all_urls():
    query = '''
        SELECT
            id,
            name,
            created_at
        FROM urls
        ORDER BY id DESC
        '''
    with make_db_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()


def get_url_by_name(url):
    query = '''
        SELECT *
        FROM urls
        WHERE name=%s
        '''
    with make_db_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (url,))
            return cursor.fetchone()


def get_url_by_id(id_):
    query = '''
        SELECT *
        FROM urls
        WHERE id=%s
        '''
    with make_db_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (id_,))
            return cursor.fetchone()
