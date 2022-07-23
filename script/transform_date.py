
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from pandas import Series


def transform_date(date: 'Series') -> 'Series':
    return pd.to_datetime(date)
