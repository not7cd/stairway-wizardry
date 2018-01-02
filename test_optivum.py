import datetime
import json
from bs4 import BeautifulSoup

from optivum import timetable_scraper, timetable_parser

sitemap_html = '''<html>
<body>
Plan aktualny od 2017-11-06</br></br>
<div class="logo">
<img border="0" src="=f" alt="">
</div>
<h4>Oddziały</h4>
<ul>
<li><a href="plany/o1.html" target="plan">1A</a></li>
<li><a href="plany/o2.html" target="plan">1B</a></li>
<li><a href="plany/o3.html" target="plan">1C</a></li>
</ul>
<h4>Nauczyciele</h4>
<ul>
<li><a href="plany/n1.html" target="plan">KB</a></li>
<li><a href="plany/n2.html" target="plan">JC</a></li>
<li><a href="plany/n3.html" target="plan">SC</a></li>
</ul>
<h4>Sale</h4>
<ul>
<li><a href="plany/s1.html" target="plan">S_7</a></li>
<li><a href="plany/s2.html" target="plan">S_8</a></li>
<li><a href="plany/s3.html" target="plan">S_9</a></li>
</ul>
</body>
</html>
'''


def test_get_sitemap_date():
    sitemap = BeautifulSoup(sitemap_html, 'html.parser')
    assert timetable_scraper.get_sitemap_date(sitemap) == datetime.datetime(year=2017, month=11, day=6)

def test_reduce_diff():
    with open('timetable.json') as file:
        timetable = json.load(file)

    reduced = timetable_parser.reduce_timetable(timetable)

    assert reduced[0] != reduced[1]
    assert reduced[0] != reduced[2]
    assert reduced[0] != reduced[3]
    assert reduced[0] != reduced[4]

def test_reduce_len():
    with open('timetable.json') as file:
        timetable = json.load(file)

    reduced = timetable_parser.reduce_timetable(timetable)

    assert len(reduced) == 5
    


