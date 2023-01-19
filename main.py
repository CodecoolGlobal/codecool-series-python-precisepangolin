import json

from flask import Flask, render_template, url_for, redirect, request
from data import queries
import math
from dotenv import load_dotenv

load_dotenv()
app = Flask('codecool_series')

SHOWS_PER_PAGE = 15
SHOWN_PAGE_NUMBER = 5


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/actors')
def actors():
    actors = queries.get_actors()
    return render_template('actors.html', actors=actors)


@app.route('/shows/most-rated/')
@app.route('/shows/order-by-<order_by>-<order>')
def shows_redirect():
    return redirect(url_for('most_rated', order_by="rating", order="DESC", page_number=1))




@app.route('/filter-actors', methods=['GET', 'POST'])
def filter_actors(chosen_genre="Action", name=" "):
    genres = queries.get_genres()
    chosen_genre = request.args.get('genre')
    if chosen_genre is None:
        chosen_genre = "Action"
    print(f"Genre: '{chosen_genre}'")
    name = request.args.get('name')
    if name is None:
        name = ""
    print(f"Name: '{name}'")
    actors = queries.get_filtered_actors(chosen_genre, name)

    return render_template('filter-actors.html', actors=actors, genres=genres,
                           chosen_genre=chosen_genre, name=name)


@app.route('/ordered-shows')
@app.route('/ordered-shows/<order>')
def ordered_shows(order="DESC"):
    movies = queries.get_ordered_shows(order)
    for movie in movies:
        movie['rating_stars'] = round(movie['rating']) * "*"
    return render_template('ordered-shows.html', movies=movies, order=order)


@app.route('/shows/most-rated/<int:page_number>')
@app.route('/shows/order-by-<order_by>')
@app.route('/shows/order-by-<order_by>/<int:page_number>')
@app.route('/shows/order-by-<order_by>-<order>/<int:page_number>')
def most_rated(order_by="rating", order="DESC", page_number=1):
    # shows = queries.get_most_rated()
    # title, year, runtime, and rating co
    if order_by not in ["title", "rating", "year", "runtime"]:
        return render_template('error.html')

    shows = queries.get_shows_details(order_by, order, page_number, SHOWS_PER_PAGE)

    count = queries.get_shows_count()
    page_count = int(count['count']) // SHOWS_PER_PAGE
    shown_page_start = page_number - ((SHOWN_PAGE_NUMBER - 1) // 2)
    shown_page_end = page_number + ((SHOWN_PAGE_NUMBER - 1) // 2)
    if shown_page_start < 1:
        shown_page_start = 1
        shown_page_end = SHOWN_PAGE_NUMBER
    elif shown_page_end > page_count:
        shown_page_start = page_count - SHOWS_PER_PAGE + 1
        shown_page_end = page_count

    return render_template(
        'most-rated.html',
        shows=shows,
        order=order,
        order_by=order_by,
        page_number=page_number,
        shown_page_end=shown_page_end,
        shown_page_start=shown_page_start,
        page_count=page_count)


@app.route('/api/show/<id>')
def api_get_show(id):
    show_details = queries.get_show_details(id)
    return json.dumps(show_details)


@app.route('/shows/<int:show_id>/actors')
def show_actors(show_id):
    shows_actors = queries.get_actors_by_show(show_id)
    show_details = queries.get_show_title(show_id)[0]
    return render_template('shows_actors.html', actors=shows_actors, show=show_details)




@app.route('/shows/<show_id>')
def detailed_view(show_id):
    show_details = queries.get_show_details(show_id)
    genres = queries.get_show_genres(show_id)
    seasons = queries.get_show_seasons(show_id)
    runtime = show_details['runtime']
    h, m = divmod(runtime, 60)
    runtime_str = (str(h) + 'h ' if h else '') + (str(m) + 'm ' if m else '')

    show_details['runtime'] = runtime_str
    if show_details['trailer'] is not None:
        show_details['video_id'] = show_details['trailer'][show_details['trailer'].find('=') + 1:]
    else:
        show_details['video_id'] = None;

    return render_template('detailed-view.html', show_detail=show_details,
                           genres=genres, seasons=seasons)


@app.route('/ratings')
def ratings_list():
    movies = queries.get_ten_movies()
    shows = queries.get_shows()
    ratings = []
    for show in shows:
        ratings.append(show['rating'])

    avg_rating = sum(ratings) / len(ratings)
    for movie in movies:
        movie['avg'] = "{:.2f}".format(movie['rating'] - avg_rating)
        if movie['rating'] - avg_rating > 0:
            movie['avg'] = "+" + movie['avg']
    return render_template('ratings.html', movies=movies)

@app.route('/actors/<int:actor_id>')
def actor_details(actor_id):
    actor = queries.get_actor_by_id(actor_id)[0]
    return render_template('actor-details.html', actor=actor)

@app.route('/birthday-actors')
def birthday_actors():
    actors = queries.get_birthday_actors()
    return render_template('birthday-actors.html', actors=actors)


def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
