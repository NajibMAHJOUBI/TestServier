
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import Series


def str_fillna(series: 'Series', value: str = '') -> 'Series':
    return series.fillna(value=value)
