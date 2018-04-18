'''
music_jawn_app.main
-------------------
Starting point and main functionality of music jawn app.

'''


from flask import Flask, render_template
from flask_bootstrap import Bootstrap

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
    }
    return render_template('map.html', **context)


@app.route("/timeline/")
def timeline():
    context = {
        'title': 'Timeline',
    }
    return render_template('timeline.html', **context)
