from functools import reduce
import json

def adfasdsdg(li, elt):
    i = elt.pop('w')
    k = elt.pop('g')
    s = elt.pop('s')
    
    li[i][k] = li[i].get(k, {})
    li[i][k][s] = elt

    return li


def reduce_timetable(timetable):
    return reduce(adfasdsdg, timetable['lessons'], [{}]*5)



if __name__ == '__main__':
    with open('timetable.json') as file:
        timetable = json.load(file)

    reduced = reduce_timetable(timetable)

    with open('reduced.json', 'w') as file:
        json.dump(reduced, file)
    print(reduced)