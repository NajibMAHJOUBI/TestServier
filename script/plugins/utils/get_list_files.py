import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from airflow.models.taskinstance import TaskInstance


def get_list_files(path_data: str, ti: 'TaskInstance'):
    list_json, list_csv = list(), list()
    for file in os.listdir(path_data):
        if file.endswith(".csv"):
            list_csv.append(os.path.join(path_data, file))
        elif file.endswith(".json"):
            list_json.append(os.path.join(path_data, file))

    ti.xcom_push(key='csv', value=list_csv)
    ti.xcom_push(key='json', value=list_json)
