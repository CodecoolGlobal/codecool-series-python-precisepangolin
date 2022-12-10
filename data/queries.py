from data import data_manager
from psycopg2 import sql

def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_most_rated():
    query = """
    SELECT shows.id AS id, title, year, runtime, TO_CHAR(rating::float,'999.9') AS rating, 
    STRING_AGG (genres.name, ', ' ORDER BY genres.name ) AS genres, trailer, homepage
    FROM shows
    JOIN show_genres ON shows.id = show_genres.show_id
    JOIN genres ON show_genres.genre_id = genres.id
    GROUP BY shows.id
    ORDER BY rating DESC
    LIMIT 15
    """
    return data_manager.execute_select(query)


def get_shows_count():
    query = """
    select count(*) as count from shows"""
    return data_manager.execute_select(query, None, False)

def get_shows_details(order_by, order="DESC", page_number=1, shows_per_page=15):
    query = sql.SQL("""
    SELECT shows.id AS id, title, TO_CHAR(year, 'YYYY Mon DD') AS year, runtime, TO_CHAR(rating::float,'999.9') AS rating, 
    STRING_AGG (genres.name, ', ' ORDER BY genres.name ) AS genres, trailer, homepage
    FROM shows
    JOIN show_genres ON shows.id = show_genres.show_id
    JOIN genres ON show_genres.genre_id = genres.id
    GROUP BY shows.id
    ORDER BY 
        CASE WHEN %(order)s = 'ASC' THEN {order_by} END ASC,
        CASE WHEN %(order)s = 'DESC' THEN {order_by} END DESC
    LIMIT %(limit)s
    OFFSET %(offset)s
    """).format(order_by=sql.Identifier(order_by))
    return data_manager.execute_select(query, {"order": order, "limit":shows_per_page, "offset": (page_number - 1 ) * shows_per_page})

def get_show_details(show_id):
    query = """
    SELECT shows.id AS id, title,
       STRING_AGG(actors.name, ', ' ORDER BY actors.name) AS actors,
       TO_CHAR(year, 'DD Mon YYYY') AS year,
       runtime,
       TO_CHAR(rating::float,'999.9') AS rating,
       overview, trailer, homepage
    FROM shows
    INNER JOIN show_characters ON shows.id = show_characters.show_id
    INNER JOIN actors ON show_characters.actor_id = actors.id
    WHERE shows.id = %(show_id)s
    GROUP BY shows.id
    """
    return data_manager.execute_select(query,
                                       {"show_id": show_id}, False)


def get_show_ganres(show_id):
    query = """
    SELECT shows.id AS id,
       STRING_AGG(genres.name, ', ' ORDER BY genres.name) AS genres
    FROM shows
    JOIN show_genres ON shows.id = show_genres.show_id
    JOIN genres ON show_genres.genre_id = genres.id
    WHERE shows.id = %(show_id)s
    GROUP BY shows.id;
    """
    return data_manager.execute_select(query,
                                       {"show_id": show_id}, False)

def get_show_seasons(showid):
    query = """
    SELECT season_number as number, title, overview
FROM seasons
WHERE show_id = %(showid)s
ORDER BY season_number"""
    return data_manager.execute_select(query, {"showid": showid})