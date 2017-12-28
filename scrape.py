import os
import json
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs


def extract_id(path):
    a = urlparse(path)
    b = os.path.basename(a.path)
    c = os.path.splitext(b)[0]
    return c


def get_url_id(soup, class_):
    return extract_id(soup.find('a', class_=class_)['href'])


def dict_from_list(ul):
    return {get_url_id(li, None): li.a.string for li in ul.find_all('li')}
    

def get_lesson(soup):
    n = get_url_id(soup, 'n') # nauczyciel
    o = get_url_id(soup, 'o') # odział, klasa
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
        response = requests.get(base_url+'/plany/' + classroom + '.html')
        table = bs(response.text, 'html.parser').find('table', class_='tabela')
        for lesson in get_classroom_lessons(table):
            yield {'s':classroom, **lesson} 


def translate_internal_id(lesson, o, n, s):
    lesson['o'] = o[lesson['o']]
    lesson['n'] = n[lesson['n']]
    lesson['s'] = s[lesson['s']].lower()
    return lesson


def get_sitemap(base_url):
    response = requests.get(base_url + 'lista.html')
    sitemap = bs(response.text, 'html.parser')
    return (dict_from_list(ul) for ul in sitemap.find_all('ul'))


def get_schedule(base_url):
    units, teachers, classrooms = get_sitemap(base_url)
    for lesson in get_all_lessons(base_url, classrooms):
        # print(lesson)
        lesson = translate_internal_id(lesson, units, teachers, classrooms)
        print(lesson)
        yield lesson


if __name__ == '__main__':
    BASE_URL = 'http://ilo.gda.pl/src/plan/'
    with open('schedule.json', 'w') as file:
        result = get_schedule(BASE_URL)
        json.dump(list(result), file)
