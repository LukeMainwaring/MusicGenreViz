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
        city_data = [city for city in result]
        # print(city_data)

    #context = {
    #    'title': 'Map',
    #    'city_data': city_data,
    #}
    #return render_template('map.html', **context)

    # testing without context and title
    return render_template('map.html', city_data=city_data)


@app.route("/timeline/")
def timeline():
    context = {
        'title': 'Timeline',
        'data' : [{'genre': 'pop', 'percent': 0.1611}, 
                            {'genre': 'rap', 'percent': 0.1099},
                            {'genre': 'trap music', 'percent': 0.0807},
                            {'genre': 'dance pop', 'percent': 0.0597},
                            {'genre': 'pop rap', 'percent': 0.0546},
                            {'genre': 'post-teen pop', 'percent': 0.0524},
                            {'genre': 'southern hip hop', 'percent': 0.0472},
                            {'genre': 'contemporary country', 'percent': 0.0375},
                            {'genre': 'hip hop', 'percent': 0.0341},
                            {'genre': 'country road', 'percent': 0.0256}]
    }
    return render_template('timeline.html', **context)
