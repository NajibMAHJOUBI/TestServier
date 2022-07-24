import os
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from airflow.models.taskinstance import TaskInstance


def extract_csv_to_df(dir_extract: str, ti: 'TaskInstance') -> None:
    """
    Extraction des fichier CSV

    Parameters
    ----------
    dir_extract: répertoire de sauvegarde de l'extraction
    ti: airflow task instance

    Returns
    -------
    None
    """
    list_csv = ti.xcom_pull(task_ids='get_list_files', key='csv')
    dfs = [pd.read_csv(path, dtype=str).rename(columns={'scientific_title': 'title'}) for path in list_csv]
    df = pd.concat(dfs, ignore_index=True)
    path_extract = os.path.join(dir_extract, 'extract_csv.csv')
    df.to_csv(path_extract, index=False)

    ti.xcom_push(key='csv', value=path_extract)
