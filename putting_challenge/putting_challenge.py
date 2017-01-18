# -*- coding: utf-8 -*-
from contextlib import contextmanager
from falcon import HTTP_404, HTTP_204

import hug
import psycopg2
import psycopg2.pool

api = hug.http(prefixes='/api')

db = psycopg2.pool.SimpleConnectionPool(1,10,
    dbname='putting-challenge',
    user='scott',
    password='tiger',
    host='localhost',
    port=5432
)

@contextmanager
def get_cursor():
    """A ContextManager for getting a cursor"""
    try:
        conn = db.getconn()
        with conn: # ensure commit or rollback
            with conn.cursor() as cur:
               yield cur
    except:
        raise
    finally:
        db.putconn(conn)

@api.get('/scorecards')
def get_scorecards():
    '''Returns a json list of scorecards'''
    scorecards = {}
    with get_cursor() as cur:
        cur.execute("SELECT * FROM scorecards;")
        scorecards = cur.fetchall()
    return scorecards

@api.get('/scorecards/{id}')
def get_scorecard(id: hug.types.number, response):
    '''Returns the scorecard requested by "id" in json format'''
    select = "SELECT * FROM scorecards WHERE id = {id}".format(id=id)
    with get_cursor() as cur:
        cur.execute(select)
        scorecard = cur.fetchone()
    if scorecard is None:
        response.status = HTTP_404
    return scorecard

@api.post('/scorecards')
def create_scorecard(body):
    '''Create a new scorecard'''
    id = ''
    with get_cursor() as cur:
        cur.execute("""
            INSERT INTO scorecards (
                timestamp,
                grand_total,
                station_1,
                station_2,
                station_3,
                station_4,
                station_5,
                raw
            )
            VALUES (
                {timestamp},
                {grand_total},
                {station_1},
                {station_2},
                {station_3},
                {station_4},
                {station_5},
                {raw}
            )
            RETURNING id;
        """.format(
            timestamp=body['timestamp'],
            grand_total=body['grand_total'],
            station_1=body['station_1'],
            station_2=body['station_2'],
            station_3=body['station_3'],
            station_4=body['station_4'],
            station_5=body['station_5'],
            raw=body['raw']
        ))
        id = cur.fetchone()[0]
    return id

@api.delete('/scorecards/{id}')
def delete_scorecard(id: hug.types.number, response):
    '''Deletes the scorecard requested by "id"'''
    delete = "DELETE FROM scorecards WHERE id = {}".format(id=id)
    with get_cursor() as cur:
        cur.execute(delete)
        cur.commit()
    response.status = HTTP_204
    return ''
