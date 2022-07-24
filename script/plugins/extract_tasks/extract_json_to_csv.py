import os
from typing import TYPE_CHECKING

import json5
import pandas as pd

if TYPE_CHECKING:
    from airflow.models.taskinstance import TaskInstance


def extract_json_to_df(dir_extract: str, ti: 'TaskInstance') -> None:
    """
    Extraction des fichier JSON

    Parameters
    ----------
    dir_extract: répertoire de sauvegarde de l'extraction
    ti: airflow task instance

    Returns
    -------
    None
    """
    list_json = ti.xcom_pull(task_ids='get_list_files', key='json')
    dfs = list()
    for path in list_json:
        with open(path) as f:
            data = json5.load(f)
            dfs.append(pd.DataFrame(data))
    df = pd.concat(dfs, ignore_index=True)

    path_extract = os.path.join(dir_extract, 'extract_json.csv')
    df.to_csv(path_extract, index=False)

    ti.xcom_push(key='json', value=path_extract)
