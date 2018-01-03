import os
import json
import requests
import dateutil.parser as dparser
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs


def get_soup(url):
    response = requests.get(url)
    return bs(response.content.decode('utf-8','ignore'), 'html.parser')


def extract_id(path):
    # Just easy as
    a = urlparse(path)
    b = os.path.basename(a.path)
    c = os.path.splitext(b)[0]
    # That's how you make it right!
    return c


def get_url_id(soup, class_):
    return extract_id(soup.find('a', class_=class_)['href'])

def get_url_ids(soup, class_):
    return [extract_id(elt['href']) for elt in soup.find_all('a', class_=class_)]


def dict_from_list(ul):
    return {get_url_id(li, None): li.a.string for li in ul.find_all('li')}
    

def get_lesson(soup):
    n = get_url_id(soup, 'n') # nauczyciel
    o = get_url_ids(soup, 'o') # odział, klasa
    p = soup.find('span', class_='p').string # przedmiot
    return {'n': n, 'o': o, 'p':p}


def get_classroom_lessons(table):
    rows = table.find_all('tr')
    for row in rows[1:]:
        hours = row.find(class_='g').string
        for weekday, lesson in enumerate(row.find_all(class_='l')):
            try:
                yield {'w': weekday, 'g': hours, **get_lesson(lesson)}
            except TypeError:
                pass


def get_all_lessons(base_url, classrooms):
    for classroom in classrooms:
        table = get_soup(base_url + '/plany/' + classroom + '.html').find('table', class_='tabela')
        for lesson in get_classroom_lessons(table):
            yield {'s':classroom, **lesson} 


def translate_internal_id(lesson, o, n, s):
    lesson['o'] = list(map(lambda elt: o[elt], lesson['o']))
    lesson['n'] = n[lesson['n']]
    lesson['s'] = s[lesson['s']]
    return lesson


def parse_sitemap(sitemap):
    return (dict_from_list(ul) for ul in sitemap.find_all('ul'))


def get_sitemap_date(sitemap):
    return dparser.parse(sitemap.body.string, fuzzy=True)


def get_timetable(base_url):
    sitemap = get_soup(base_url + 'lista.html')

    date_valid = get_sitemap_date(sitemap)
    units, teachers, classrooms = parse_sitemap(sitemap)

    result = {'valid_from': '{:%Y-%m-%d}'.format(date_valid), 'lessons': []}

    for lesson in get_all_lessons(base_url, classrooms):
        
        lesson = translate_internal_id(lesson, units, teachers, classrooms)
        print(lesson)
        result['lessons'].append(lesson)

    return result

def get_actual(path, url):
    with open(path, encoding="utf-8") as file:
        timetable = json.load(file)

    d1 = dparser.parse(timetable['valid_from'])
    d2 = get_sitemap_date(get_soup(url + 'lista.html'))

    # print(d1, d2)

    if d1 >= d2:
        print('using cached')
        return timetable
    else:
        print('scraping new')
        return get_timetable(url)



if __name__ == '__main__':
    BASE_URL = 'http://ilo.gda.pl/src/plan/'
    result = get_timetable(BASE_URL)
    with open('data/timetable.json', 'w', encoding="utf-8") as file:
        json.dump(result, file)
