import json
import os

from flask import Flask, request, send_from_directory, render_template, jsonify
from optivum import timetable_parser, timetable_scraper


app = Flask(__name__, static_url_path='')


timetable = timetable_scraper.get_actual('data/timetable.json', 'http://ilo.gda.pl/src/plan/')
# print(timetable)
data = timetable_parser.reduce_timetable(timetable)

@app.route("/svg")
def plain_svg():
    """Sends only svg"""
    return send_from_directory('templates', 'plan.svg')

@app.route('/')
def index():
    """Index view"""
    return render_template('index.html')

@app.route('/data')
def data_json():
    """REST data"""
    return jsonify(data)

app.route('/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(debug=True, port=port)
