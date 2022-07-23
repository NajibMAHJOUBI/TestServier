from typing import List
from typing import TYPE_CHECKING

import pandas as pd

from reduce_dict import reduce_dict
from lower_case import lower_case
from str_fillna import str_fillna
from sub_unicode import sub_unicode
from transform_date import transform_date

if TYPE_CHECKING:
    from pandas import DataFrame


def transform(data: 'DataFrame', drugs_list: List[str]) -> 'DataFrame':
    data.rename(columns={'scientific_title': 'title'}, inplace=True)

    data['date'] = transform_date(data['date']).astype(str)

    data['title'] = lower_case(data['title'])

    data['journal'] = str_fillna(data['journal'])

    data['journal'] = data['journal'].map(lambda journal: sub_unicode(journal))

    data['title_split'] = data['title'].str.split(' ')

    data['drugs'] = data['title_split'].map(lambda words: set(words).intersection(drugs_list))

    data.drop(columns=['title_split', 'title'], inplace=True)

    data = data[data['drugs'].str.len() >= 1]

    data = data.explode('drugs')

    data['values'] = data.apply(lambda row: {row['journal']: {str(row['date']): [row['id']]}},
                                                         axis=1)

    return data


def concatenate_data(dfs: List['DataFrame']):
    all_data = pd.concat(dfs)
    return all_data.groupby('drugs').agg({'values': reduce_dict}).reset_index()

