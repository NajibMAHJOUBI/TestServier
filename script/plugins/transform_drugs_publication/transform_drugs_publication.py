import os
import re
import uuid

from typing import List
from typing import TYPE_CHECKING

import pandas as pd
import nltk
nltk.download('stopwords')

if TYPE_CHECKING:
    from airflow.models.taskinstance import TaskInstance


def get_drugs_list(path_data: str) -> List[str]:
    drugs = pd.read_csv(path_data)
    return drugs['drug'].str.lower().values.tolist()


def get_list_extract(ti: 'TaskInstance') -> List[str]:
    list_files = list()
    list_files.append(ti.xcom_pull(task_ids='extract_json_to_df', key='json'))
    list_files.append(ti.xcom_pull(task_ids='extract_csv_to_df', key='csv'))
    return list_files


def transform_drugs_publication(path_drugs: str, path_work: str, ti: 'TaskInstance'):
    drugs_list = get_drugs_list(path_drugs)
    print(drugs_list)

    data = pd.concat([pd.read_csv(path) for path in get_list_extract(ti)], ignore_index=True)

    # data['id'] = pd.Series([uuid.uuid4() for _ in range(data.shape[0])])

    data['date'] = pd.to_datetime(data['date']).astype(str)

    data['title_split'] = data['title'].str.replace(r'[^\w\s]+', ' ')

    data['title_split'] = data['title_split'].str.lower()

    data['journal'] = data['journal'].fillna(value='')

    data['journal'] = data['journal'].map(lambda journal: re.sub(r'(\\xc3)|(\\x28)', '', journal))

    data['title_split'] = data['title_split'].str.split(' ')

    stop_words = nltk.corpus.stopwords.words('english') + ['']
    data['title_split'] = data['title_split'].map(
        lambda words: [word for word in words if word not in stop_words])

    data['drugs'] = data['title_split'].map(lambda words: set(words).intersection(drugs_list))

    data.drop(columns=['title_split'], inplace=True)

    data = data[data['drugs'].str.len() >= 1]

    data = data.explode('drugs')

    data.rename(columns={'drugs': 'drug'}, inplace=True)

    # data['values'] = data.apply(lambda row: {row['journal']: {str(row['date']): [row['id']]}}, axis=1)

    # data = data.groupby('drugs').agg({'values': reduce_dict}).reset_index()

    path_transform = os.path.join(path_work, "transform_drugs.csv")

    data.to_csv(path_transform, index=False)

    ti.xcom_push(key='transform', value=path_transform)
