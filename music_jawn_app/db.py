'''
music_jawn_app.db
-----------------
Functions to interact with the MySQL database on AWS.

'''


import functools
import json
import traceback

from flask import g

import pymysql
import pymysql.cursors


def require_connection(db_function):
    '''
    Route decorator to require a database connection and closes after.

    '''
    @functools.wraps(db_function)
    def wrapper(*args, **kwargs):
        if not hasattr(g, 'db_connection') or not g.db_connection.open:
            g.db_connection = pymysql.connect(
                                host='cis550-2.cmxt8otwhjqc.us-east-2.rds.amazonaws.com',
                                db='cis550',
                                user='cis550',
                                password='cis550eklh',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
        result = db_function(*args, **kwargs)
        g.db_connection.close()
        return result
    return wrapper


@require_connection
def db_query(query, **query_params):
    '''
    Decorator to query the database.

    '''
    try:
        with g.db_connection.cursor() as cursor:
            cursor.execute(query, **query_params)
            result = cursor.fetchall()
            if len(result) == 0:
                raise RuntimeError('No results found.')
            return result
    except Exception:
        print('\nError - unable to complete the below query: \n{}\n\n'.format(query))
        traceback.print_exc()
        return None


def cache(cache_file):
    '''
    Decorator for caching database query results.

    Allows chaining through packing query params into the 'iter' kwarg.

    '''
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try:
                with open('static/cache/' + cache_file) as data_file:
                    print('Found cache for \'{}\''.format(cache_file))
                    data = json.loads(data_file.read())
                    return data
            except FileNotFoundError:
                print('No cache available for \'{}\''.format(cache_file))
                print('Querying database...')
                result = function(*args, **kwargs)
                # cache result
                with open('static/cache/' + cache_file, mode='w') as data_file:
                    print('Writing file to cache')
                    data_file.write(json.dumps(result))
                return result
        return wrapper
    return decorator


## Queries

@cache('all_city_genres.txt')
def all_city_genres():
    cities = db_query('SELECT * FROM city')
    if cities is None:
        return None
    for city in cities:
        genres = top_genres_by_city(city['city_id'])
        if genres is not None:
            city['genres'] = genres
    return cities


def top_genres_by_city(city_id):
    '''
    Return the top 10 genres by percentile for a given city.
    '''
    sql_file_path = 'static/sql/top_genres_by_city.sql'
    try:
        with open(sql_file_path) as file:
            query = file.read()
    except FileNotFoundError:
        print('Could not find file \'{}\''.format(sql_file_path))
        return None

    result = db_query(query.format(city_id=city_id))
    if result is not None:
        result = [{'genre': x['genre'], 'percent': round(float(x['percent']) * 100, 2)} 
                  for x in result]
        return result


@cache('all_year_genres.txt')
def all_year_genres():
    years = db_query('SELECT DISTINCT year FROM artist_rank')
    if years is None:
        return None
    years = sorted([x.get('year') for x in years])
    genres_by_year = []
    for year in years:
        genres = top_genres_by_year(year)
        if genres is not None:
            genres_by_year.append({
                'year': year,
                'genres': genres
                })
    return genres_by_year


def top_genres_by_year(year):
    ''' 
    Return the top 10 genres by percentile for a given year.
    '''
    sql_file_path = 'static/sql/top_genres_by_year.sql'
    try:
        with open(sql_file_path) as file:
            query = file.read()
    except FileNotFoundError:
        print('Could not find file \'{}\''.format(sql_file_path))
        return None

    result = db_query(query.format(year=year))
    if result is not None:
        result = [{'genre': x['genre'], 'percent': round(float(x['percent']) * 100, 2)} 
                  for x in result]
        return result

