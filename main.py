from flask import Flask, render_template, url_for
from data import queries
import math
import json
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


@app.route('/api/shows/order-by-<order_by>')
@app.route('/api/shows/order-by-<order_by>-<order>')
def api_most_rated(order_by="rating", order="DESC"):
    shows = queries.get_shows_details(order_by, order)
    return render_template('most-rated-api.html', shows=shows, order = order, order_by = order_by)


@app.route('/api/json/shows/order-by-<order_by>')
@app.route('/api/json/shows/order-by-<order_by>-<order>')
def api_json_most_rated(order_by="rating", order="DESC"):
    shows = queries.get_shows_details(order_by, order)
    return json.dumps(shows)



@app.route('/shows/most-rated')
@app.route('/shows/most-rated/<int:page_number>')
@app.route('/shows/order-by-<order_by>')
@app.route('/shows/order-by-<order_by>/<int:page_number>')
@app.route('/shows/order-by-<order_by>-<order>')
@app.route('/shows/order-by-<order_by>-<order>/<int:page_number>')
def most_rated(order_by="rating", order="DESC", page_number = 1):
    count = queries.get_shows_count()
    page_count = int(count['count']) // SHOWS_PER_PAGE
    shown_page_start = page_number - ((SHOWN_PAGE_NUMBER - 1 )// 2)
    shown_page_end = page_number + ((SHOWN_PAGE_NUMBER - 1 )// 2)
    if shown_page_start < 1:
        shown_page_start = 1
        shown_page_end = SHOWN_PAGE_NUMBER
    elif shown_page_end > page_count:
        shown_page_start = page_count - SHOWS_PER_PAGE + 1
        shown_page_end = page_count

    #shows = queries.get_most_rated()
    # title, year, runtime, and rating co
    if order_by not in ["title", "rating", "year", "runtime"]:
        return render_template('error.html')


    shows = queries.get_shows_details(order_by, order, page_number, SHOWS_PER_PAGE)
    return render_template(
        'most-rated.html',
        shows=shows,
        order = order,
        order_by = order_by,
        page_number=page_number,
        shown_page_end = shown_page_end,
        shown_page_start=shown_page_start,
        page_count = page_count)


@app.route('/api/show/<id>')
def api_get_show(id):
    show_details = queries.get_show_details(id)
    return json.dumps(show_details)
    #return json
@app.route('/shows/<show_id>')
def detailed_view(show_id):
    show_details = queries.get_show_details(show_id)
    ganres = queries.get_show_ganres(show_id)
    seasons = queries.get_show_seasons(show_id)
    runtime = show_details['runtime']
    h, m = divmod(runtime, 60)
    runtime_str = (str(h) + 'h ' if h else '') + (str(m) + 'm ' if m else '')

    show_details['runtime'] = runtime_str
    show_details['video_id'] = show_details['trailer'][show_details['trailer'].find('=') + 1:]

    return render_template('detailed-view.html', show_detail=show_details,
                           ganres=ganres, seasons=seasons)


def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()