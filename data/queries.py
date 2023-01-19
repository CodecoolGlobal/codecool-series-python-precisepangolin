from data import data_manager
from psycopg2 import sql


def get_actors():
    query = """
    SELECT actors.name as name, actors.id as actor_id, STRING_AGG (shows.title, ', ' ORDER BY shows.title ) AS movies, 
    JSON_OBJECT_AGG(shows.id, shows.title) as show_details
    FROM actors
    FULL JOIN show_characters on actors.id = show_characters.actor_id
    FULL JOIN shows on show_characters.show_id = shows.id
    GROUP BY actors.id, name
    ORDER BY name ASC
    LIMIT 20

    """
    return data_manager.execute_select(query)


def get_shows():
    return data_manager.execute_select("SELECT id, title, ROUND(rating::numeric,2) AS rating FROM shows;")


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


def get_show_title(show_id):
    query = """
    SELECT title
    FROM shows
    WHERE id = %(show_id)s
    """
    return data_manager.execute_select(query, {"show_id": show_id})


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
    return data_manager.execute_select(query, {"order": order, "limit": shows_per_page,
                                               "offset": (page_number - 1) * shows_per_page})


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


def get_show_genres(show_id):
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


def get_ten_movies():
    query = """
    SELECT title, ROUND(rating::numeric,2) AS rating
    FROM shows
    FULL JOIN show_characters on shows.id = show_characters.show_id
    GROUP BY title, rating
    ORDER BY count(actor_id) DESC
    LIMIT 10"""
    return data_manager.execute_select(query)


def get_ordered_shows(order):
    query = """
    SELECT shows.title, ROUND(shows.rating::numeric,0) AS rating, count(DISTINCT episodes.id) AS episode_count
    FROM shows
    FULL JOIN seasons on shows.id = seasons.show_id
    FULL JOIN episodes on episodes.season_id = seasons.id
    GROUP BY shows.title, shows.rating
    ORDER BY
    CASE WHEN %(order)s = 'ASC' THEN count(DISTINCT episodes.id) END ASC,
    CASE WHEN %(order)s = 'DESC' THEN count(DISTINCT episodes.id) END DESC
    LIMIT 10"""
    return data_manager.execute_select(query, {"order": order})


def get_genres():
    query = """
    SELECT name, id
    FROM genres
    WHERE name != 'None'
    ORDER BY name ASC"""
    return data_manager.execute_select(query)


def get_actors_by_show(show_id):
    query = """
    SELECT actors.name, actors.id, show_characters.character_name as character_name
    FROM actors
    FULL JOIN show_characters on actors.id = show_characters.actor_id
    WHERE show_id = %(show_id)s
    ORDER BY actors.name
    """
    return data_manager.execute_select(query, {"show_id": show_id})


def get_actor_by_id(actor_id):
    query = """
    SELECT *
    FROM actors
    WHERE id = %(actor_id)s"""
    return data_manager.execute_select(query, {"actor_id": actor_id})


def get_filtered_actors(genre, name):
    query = """
    SELECT actors.name, STRING_AGG (DISTINCT genres.name, ', ' ORDER BY genres.name ) AS genres
    FROM actors
    FULL JOIN show_characters on actors.id = show_characters.actor_id
    FULL JOIN show_genres on show_genres.show_id = show_characters.show_id
    FULL JOIN genres on show_genres.genre_id = genres.id
    WHERE genres.name LIKE %(genre)s AND actors.name ILIKE %(name)s
    GROUP BY actors.name
    LIMIT 20
    """
    return data_manager.execute_select(query, {"genre": genre, "name": '%{}%'.format(name)})


def get_birthday_actors():
    query = """
    SELECT name, birthday
    FROM actors
    WHERE death IS NULL
    ORDER BY birthday ASC
    LIMIT 100"""
    return data_manager.execute_select(query)