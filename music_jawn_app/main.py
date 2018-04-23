'''
music_jawn_app.main
-------------------
Starting point and main functionality of music jawn app.

'''


from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_table import Table, Col

import db


app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def home():
    context = {
        'title': 'Home',
    }
    return render_template('home.html', **context)


@app.route("/map/")
def map():
    context = {
        'title': 'Map',
        'city_data': db.all_city_genres()
    }
    return render_template('map.html', **context)


# Declare your table
class ItemTable(Table):
    name = Col('Name')
    description = Col('Description')


@app.route("/timeline/")
def timeline():
    context = {
        'title': 'Timeline',
        'timeline_data': db.all_year_genres()
    }
    return render_template('timeline.html', **context)