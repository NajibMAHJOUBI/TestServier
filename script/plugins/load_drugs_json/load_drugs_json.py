import json

import pandas as pd


def load_drugs_json(path_transform: str, path_load: str):
    df = pd.read_csv(path_transform)

    json_data = df.set_index('drugs').to_dict()['values']

    with open(path_load, "w") as write_file:
        json.dump(json_data, write_file, indent=2)
    write_file.close()