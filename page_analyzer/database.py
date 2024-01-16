import psycopg2
from psycopg2.extras import RealDictCursor, RealDictRow

from page_analyzer.cfg import DATABASE_URL
from typing import Any


def make_db_connection():
    return psycopg2.connect(DATABASE_URL)


def insert_url(url_data: dict) -> int:
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


def insert_url_checking_result(row_data: dict) -> None:
    query = '''
    INSERT
    INTO url_checks (url_id, created_at, status_code, h1, title, description)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    with make_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (row_data['url_id'],
                                   row_data['created_at'],
                                   row_data['status_code'],
                                   row_data['h1'],
                                   row_data['title'],
                                   row_data['description'])
                           )


def get_all_urls() -> list[RealDictRow]:
    query = '''
        SELECT
            urls.id,
            urls.created_at,
            name,
            status_code,
            MAX(url_checks.created_at) AS last_check
        FROM urls
        LEFT JOIN url_checks ON urls.id = url_checks.url_id
        GROUP BY urls.id, name, status_code
        ORDER BY urls.id DESC
        '''
    with make_db_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()


def get_url_by_field(field_name: str, field_value: Any):
    query = f'''
        SELECT *
        FROM urls
        WHERE {field_name}=%s
        '''
    with make_db_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (field_value,))
            return cursor.fetchone()


def get_url_checking_results(id_: int) -> list[RealDictRow]:
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
