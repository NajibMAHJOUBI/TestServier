import os
import re
from functools import reduce
from typing import List
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from airflow.models.taskinstance import TaskInstance


def merge_dict(dict1, dict2):
    merged = dict()
    for journal in set(list(dict1.keys()) + list(dict2.keys())):
        merged[journal] = dict()
        for date in set(list(dict1.get(journal, {}).keys()) + list(dict2.get(journal, {}).keys())):
            merged[journal][date] = dict1.get(journal, {}).get(date, []) + dict2.get(journal, {}).get(date, [])
    return merged


def reduce_dict(series):
    return reduce(lambda dict1, dict2: merge_dict(dict1, dict2), series)


def get_drugs_list(path_data: str) -> List[str]:
    drugs = pd.read_csv(path_data)
    return drugs['drug'].str.lower().values.tolist()


def get_list_extract(ti: 'TaskInstance') -> List[str]:
    list_files = list()
    list_files.append(ti.xcom_pull(task_ids='extract_json_to_df', key='json'))
    list_files.append(ti.xcom_pull(task_ids='extract_csv_to_df', key='csv'))
    return list_files


def transform_drugs_publication(path_drugs: str, path_data: str, path_work: str, ti: 'TaskInstance'):
    drugs_list = get_drugs_list(path_drugs)
    print(drugs_list)

    data = pd.concat([pd.read_csv(path) for path in get_list_extract(ti)], ignore_index=True)

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

    path_transform = os.path.join(path_work, "transform_drugs.csv")

    data.to_csv(path_transform, index=False)

    ti.xcom_push(key='transform', value=path_transform)
