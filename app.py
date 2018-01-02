import json

from flask import Flask, request, send_from_directory, render_template, jsonify
from optivum import timetable_parser


app = Flask(__name__, static_url_path='')

with open('timetable.json') as file:
    timetable = json.load(file)

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



if __name__ == '__main__':
    app.run(debug=True)
