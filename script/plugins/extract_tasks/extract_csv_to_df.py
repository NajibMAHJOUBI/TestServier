from typing import List

import pandas as pd


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
