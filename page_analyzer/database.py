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


def insert_url_checking_result(row_data):
    query = '''
    INSERT
    INTO url_checks (url_id, created_at, status_code, h1, title, description)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    with make_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (row_data['url_id'],
                                   row_data['created_at'],
                                   None, None, None, None))


def get_all_urls():
    query = '''
        SELECT
            urls.id,
            name,
            urls.created_at,
            MAX(url_checks.created_at) AS last_check
        FROM urls
        LEFT JOIN url_checks ON urls.id = url_checks.url_id
        GROUP BY urls.id, name
        ORDER BY urls.id DESC
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


def get_url_checking_results(id_):
    query = '''
            SELECT *
            FROM url_checks
            WHERE url_id=%s
            ORDER BY created_at DESC
            '''
    with make_db_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (id_,))
            return cursor.fetchall()
