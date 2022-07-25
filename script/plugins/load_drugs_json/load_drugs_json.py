import ast
import json
from functools import reduce
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


def load_drugs_json(path_save: str, ti: 'TaskInstance') -> None:
    """
    Sauvegarde au format JSON du mapping des médicaments

    Parameters
    ----------
    path_save : path de sauvegarde du fichier JSON
    ti : airflow task instance

    Returns
    -------
    None
    """
    path_transform = ti.xcom_pull(task_ids='transform_drugs_publication', key='transform')
    df = pd.read_csv(path_transform, dtype=str, usecols=['title', 'date', 'journal', 'drug'])

    df['values'] = df.apply(lambda row: {row['journal']: {str(row['date']): [row['title']]}}, axis=1)

    df = df.groupby('drug').agg({'values': reduce_dict}).reset_index()

    # df['values'] = df['values'].map(lambda value: ast.literal_eval(value))

    json_data = df.set_index('drug').to_dict()['values']

    with open(path_save, "w") as write_file:
        json.dump(json_data, write_file, indent=4)
    write_file.close()
