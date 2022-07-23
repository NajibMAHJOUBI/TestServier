import re
from functools import reduce
from typing import List

import pandas as pd


def merge_dict(dict1, dict2):
    merged = dict()
    for journal in set(list(dict1.keys()) + list(dict2.keys())):
        merged[journal] = dict()
        for date in set(list(dict1.get(journal, {}).keys()) +   list(dict2.get(journal, {}).keys())):
            merged[journal][date] = dict1.get(journal, {}).get(date, []) + dict2.get(journal, {}).get(date, [])
    return merged


def reduce_dict(series):
    return reduce(lambda dict1, dict2:merge_dict(dict1, dict2), series)


def transform_drugs_publication(path_list: List[str], path_transform: str):
    drugs = pd.read_csv('/home/data-ops/Documents/Github/TestServier/data/drugs.csv')
    drugs_list = drugs['drug'].str.lower().values.tolist()

    data = pd.concat([pd.read_csv(path) for path in path_list], ignore_index=True)

    data['date'] = pd.to_datetime(data['date']).astype(str)

    data['title'] = data['title'].str.lower()

    data['journal'] = data['journal'].fillna(value='')

    data['journal'] = data['journal'].map(lambda journal: re.sub(r'(\\xc3)|(\\x28)', '', journal))

    data['title_split'] = data['title'].str.split(' ')

    data['drugs'] = data['title_split'].map(lambda words: set(words).intersection(drugs_list))

    data.drop(columns=['title_split', 'title'], inplace=True)

    data = data[data['drugs'].str.len() >= 1]

    data = data.explode('drugs')

    data['values'] = data.apply(lambda row: {row['journal']: {str(row['date']): [row['id']]}}, axis=1)

    data = data.groupby('drugs').agg({'values': reduce_dict}).reset_index()

    data.to_csv(path_transform, index=False)
