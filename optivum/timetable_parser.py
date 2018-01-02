from functools import reduce
import json

def adfasdsdg(li, elt):
    i = elt.pop('w')
    k = elt.pop('g')
    # s = elt.pop('s')
    
    # print(i,k,s)

    li[i] = li.get(i, {})
    li[i][k] = li[i].get(k, [])
    li[i][k].append(elt)

    return li


def change_keys(elt):
    elt['id'] = elt.pop('s')
    return elt


def reduce_timetable(timetable):

    result = reduce(adfasdsdg, map(change_keys, timetable['lessons']), {})
    return result



if __name__ == '__main__':
    with open('timetable.json') as file:
        timetable = json.load(file)

    reduced = reduce_timetable(timetable)

    with open('reduced.json', 'w') as file:
        json.dump(reduced, file)
    print(reduced)