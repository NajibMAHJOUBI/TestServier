import json
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from airflow.models.taskinstance import TaskInstance


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
    df = pd.read_csv(path_transform)

    json_data = df.set_index('drugs').to_dict()['values']

    with open(path_save, "w") as write_file:
        json.dump(json_data, write_file, indent=2)
    write_file.close()
