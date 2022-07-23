import json
import re
from datetime import datetime
from functools import reduce
from typing import List

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

import sys
import os
from pathlib import Path

from extract_tasks import extract_json_to_csv

# def extract_json_to_df(paths_json: List[str], path_extract: str) -> None:
#     """
#     Extraction des fichiers json pour les concatener dans un fichier csv
#
#     Parameters
#     ----------
#     paths_json : list des path de fichier json
#     path_extract: path de sauvegarde
#
#     Returns
#     -------
#     None
#     """
#     dfs = list()
#     for path in paths_json:
#         with open(path) as f:
#             data = json5.load(f)
#             dfs.append(pd.DataFrame(data))
#     df = pd.concat(dfs, ignore_index=True)
#     df.to_csv(path_extract, index=False)


def extract_csv_to_df(paths_csv: List[str], path_extract: str) -> None:
    """
    Extraction des fichiers à pour les concatener dans un fichier csv

    Parameters
    ----------
    paths_csv : list des path de fichier json
    path_extract: path de sauvegarde

    Returns
    -------
    None
    """
    dfs = [pd.read_csv(path).rename(columns={'scientific_title': 'title'}) for path in paths_csv]
    df = pd.concat(dfs, ignore_index=True)
    df.to_csv(path_extract, index=False)


def transform_data(path_list: List[str], path_transform: str):
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


def merge_dict(dict1, dict2):
    merged = dict()
    for journal in set(list(dict1.keys()) + list(dict2.keys())):
        merged[journal] = dict()
        for date in set(list(dict1.get(journal, {}).keys()) +   list(dict2.get(journal, {}).keys())):
            merged[journal][date] = dict1.get(journal, {}).get(date, []) + dict2.get(journal, {}).get(date, [])
    return merged


def reduce_dict(series):
    return reduce(lambda dict1, dict2:merge_dict(dict1, dict2), series)


def load_to_json(path_transform: str, path_load: str):
    df = pd.read_csv(path_transform)

    json_data = df.set_index('drugs').to_dict()['values']

    with open(path_load, "w") as write_file:
        json.dump(json_data, write_file, indent=2)
    write_file.close()


list_csv_files = ['/home/data-ops/Documents/Github/TestServier/data/clinical_trials.csv',
                  '/home/data-ops/Documents/Github/TestServier/data/pubmed.csv']
list_json_files = ['/home/data-ops/Documents/Github/TestServier/data/pubmed.json']

path_extract_csv = '/home/data-ops/Documents/Github/TestServier/data_extract/extract_csv.csv'
path_extract_json = '/home/data-ops/Documents/Github/TestServier/data_extract/extract_json.csv'

path_transform = '/home/data-ops/Documents/Github/TestServier/data_transform/drugs_mapping.csv'

path_load = '/home/data-ops/Documents/Github/TestServier/data_load/drugs_mapping.json'

with DAG('drugs_mapping',
         start_date=datetime(2022, 1, 1),
         schedule_interval='@daily',
         catchup=False) as dag:

    extract_json_to_df = PythonOperator(task_id='extract_json_to_df',
                                        python_callable=extract_json_to_csv.extract_json_to_df,
                                        op_kwargs={'paths_json': list_json_files, 'path_extract': path_extract_json},
                                        dag=dag)

    extract_csv_to_df = PythonOperator(task_id='extract_csv_to_df',
                                       python_callable=extract_csv_to_df,
                                       op_kwargs={'paths_csv': list_csv_files, 'path_extract': path_extract_csv},
                                       dag=dag)

    transform_data = PythonOperator(task_id='transform_data',
                                    python_callable=transform_data,
                                    op_kwargs={'path_list': [path_extract_json, path_extract_csv],
                                               'path_transform': path_transform},
                                    dag=dag)

    load_to_json = PythonOperator(task_id='load_to_json',
                                  python_callable=load_to_json,
                                  op_kwargs={'path_transform': path_transform, 'path_load': path_load},
                                  dag=dag)


[extract_json_to_df, extract_csv_to_df] >> transform_data >> load_to_json


# if __name__ == "__main__":
#     extract_csv_to_df(list_csv_files, path_extract_csv)
