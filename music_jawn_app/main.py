'''
music_jawn_app.main
-------------------
Starting point and main functionality of music jawn app.

'''


from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import pymysql
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='cis550-2.cmxt8otwhjqc.us-east-2.rds.amazonaws.com',
                             db='cis550',
                             user='cis550',
                             password='cis550eklh',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


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
    # test query
    with connection.cursor() as cursor:
        # Read a single record
        sql = '''SELECT * FROM city;'''
        cursor.execute(sql)
        result = cursor.fetchall()
        for city in result:
            print(city)

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
