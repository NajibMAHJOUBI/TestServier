from typing import List

import json5
import pandas as pd


def extract_json_to_df(paths_json: List[str], path_extract: str) -> None:
    """
    Extraction des fichiers json pour les concatener dans un fichier csv

    Parameters
    ----------
    paths_json : list des path de fichier json
    path_extract: path de sauvegarde

    Returns
    -------
    None
    """
    dfs = list()
    for path in paths_json:
        with open(path) as f:
            data = json5.load(f)
            dfs.append(pd.DataFrame(data))
    df = pd.concat(dfs, ignore_index=True)
    df.to_csv(path_extract, index=False)
