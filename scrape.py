import requests
from urllib.parse import urlparse
import os
from bs4 import BeautifulSoup as bs

from functools import reduce

BASE_URL = 'http://ilo.gda.pl/src/plan/'

class LessonTime():
    def __init__(self, time, weekday):
        self.time = time
        self.weekday = weekday

    def __repr__(self):
        return 'LessonTime(%s, %s)' % (self.time, self.weekday)


class Lesson():
    def __init__(self, subject, classroom, teacher, unit):
        self.time = None
        self.subject = subject
        self.classroom = classroom
        self.teacher = teacher
        self.unit = unit

    def __repr__(self):
        return 'Lesson({}, {}, {}, {})'.format(self.subject, self.classroom, self.teacher, self.unit)

    def from_td(self, soup):
        self.subject = soup.find('span', class_='p').string
        self.teacher = get_class_id(soup, "n")
        self.unit = get_class_id(soup, "o")

class Weekday():
    """docstring for Weekday"""
    def __init__(self, weekday):
        self.weekday = weekday
        self.lesson_hours = {}

    def __repr__(self):
        return 'Weekday({})'.format(self.weekday) + ''.join(['\n\t{!r}'.format(lh) for lh in self.lesson_hours.values()])

    def add_lesson(self, lesson, lh):
        self.lesson_hours[lh] = self.lesson_hours.get(lh, LessonHour(lh))
        self.lesson_hours[lh].add(lesson)

    def extend(self, other):
        for key in other.lesson_hours:
            self.lesson_hours[key] = self.lesson_hours.get(key, LessonHour(key)) + other.lesson_hours.get(key, LessonHour(key))

    def __add__(self, other):
        assert self.weekday == other.weekday
        w = Weekday(self.weekday)
        w.extend(self)
        w.extend(other)
        return w


class LessonHour():
    """docstring for LessonHour"""
    def __init__(self, hours):
        self.hours = hours
        self.lessons = []
        
    def __repr__(self):
        return 'LessonHour({}, [<{}> Lesson()])'.format(self.hours, len(self.lessons))

    def __add__(self, other):
        assert self.hours == other.hours
        a = LessonHour(self.hours)
        a.lessons.extend(self.lessons)
        a.lessons.extend(other.lessons)
        return a

    def add(self, lesson):
        self.lessons.append(lesson)
        


def extract_id(path):
    a = urlparse(path)
    b = os.path.basename(a.path)
    c = os.path.splitext(b)[0]
    return c


def dict_from_list(ul):
    result = {}
    for li in ul.find_all('li'):
        # print(li.a.string)
        result[extract_id(li.a['href'])] = li.a.string
    return result


def get_url_id(soup, class_):
    return extract_id(soup.find('a', class_=class_)['href'])

def get_lesson(soup):
    n = get_url_id(soup, 'n') # nauczyciel
    o = get_url_id(soup, 'o') # odział, klasa
    p = soup.find('span', class_='p') # przedmiot
    return {'n': n, 'o': o, 'p':p}


def extract_lesson(lesson_td, classroom):
    teacher = get_class_id(lesson_td, "n")
    unit = get_class_id(lesson_td, "o")
    subject = lesson_td.find('span', class_='p').string
    result = Lesson(subject, classroom, teacher, unit)
    # print(result)
    return result


def extract_table(timetable, classroom):
    rows = timetable.find_all('tr')
    header_row = rows[0]

    rows_2 = []

    weekdays = [Weekday(x) for x in range(5)]
    print(weekdays)


    for row in rows[1:]:
        hours = row.find('td', class_='g')
        lesson_tds = row.find_all('td', class_='l')

        for weekday, lesson_td in enumerate(lesson_tds):
            try:
                l = extract_lesson(lesson_td, classroom)
                print(l)
                weekdays[weekday].add_lesson(l, hours.string)
            except Exception as e:
                l = None


    for w in weekdays:
        print(w)

    return weekdays


def timetable_extractor(key):
    response = requests.get(BASE_URL+'/plany/' + key + '.html')
    timetable = bs(response.text, 'html.parser').find('table', class_='tabela')
    return extract_table(timetable, key)


def get_schedule():
    response = requests.get(BASE_URL + 'lista.html')
    sitemap = bs(response.text, 'html.parser')
    units, teachers, classrooms = (dict_from_list(ul) for ul in sitemap.find_all('ul'))
    # print([teachers[k] for k in teachers])
    weekdays = timetable_extractor('s17')
    for w in weekdays:
        print(w)
        d = input()
    

if __name__ == '__main__':
    # get_schedule()
    with open('s24.html') as f:
        t = bs(f, 'html.parser').find('table', class_='tabela')
    s24 = extract_table(t, 's24')

    with open('s30.html') as f:
        t = bs(f, 'html.parser').find('table', class_='tabela')
    s30 = extract_table(t, 's30')

    for w in list(zip(s24, s30)):
        print()

