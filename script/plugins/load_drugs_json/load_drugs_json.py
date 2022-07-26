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
    df = pd.read_csv(path_transform, dtype=str, usecols=['title', 'date', 'journal', 'drug'])

    df['publication'] = df.apply(lambda row: {'Date': row['date'], 'Titre': row['title']}, axis=1)

    df.drop(columns=['title', 'date'], inplace=True)

    df = df.groupby(['drug', 'journal']).agg(list).reset_index()

    df['citation'] = df.apply(lambda row: {'Journal': row['journal'], 'Publication': row['publication']}, axis=1)

    df.drop(columns=['journal', 'publication'], inplace=True)

    df.rename(columns={'drug': 'Medicament'}, inplace=True)

    df = df.groupby(['Medicament']).agg(list).reset_index()

    df.to_json(path_save, orient='records', indent=4)
