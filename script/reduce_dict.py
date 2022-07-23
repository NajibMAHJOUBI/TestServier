

from functools import reduce


def merge_dict(dict1, dict2):
    merged = dict()
    for journal in set(list(dict1.keys()) + list(dict2.keys())):
        merged[journal] = dict()
        for date in set(list(dict1.get(journal, {}).keys()) +   list(dict2.get(journal, {}).keys())):
            merged[journal][date] = dict1.get(journal, {}).get(date, []) + dict2.get(journal, {}).get(date, [])
    return merged


def reduce_dict(series):
    return reduce(lambda dict1, dict2:merge_dict(dict1, dict2), series)