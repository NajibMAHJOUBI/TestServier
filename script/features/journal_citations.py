import functools

import pandas as pd

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from numpy import ndarray


def publication_citations(path_data: str) -> Tuple['ndarray', int]:
    df = pd.read_json(path_data)

    df["Journal"] = df["citation"].map(lambda citation: [item['Journal'] for item in citation])

    product = functools.reduce(lambda x, y: x + y, df["Journal"])

    counts = pd.Series(product).value_counts()

    max_medicaments = counts.max()

    publication_max_medicaments = counts[counts == max_medicaments].index.values

    return publication_max_medicaments, max_medicaments


if __name__ == '__main__':
    path = '../../drugs_mapping/drugs_mapping.json'
    publications, max_medicaments = publication_citations(path)

    print(f"\nPublication citant le plus de médicaments distincts ({max_medicaments}) : ")
    for publication in publications:
        print(f"   - {publication}")
