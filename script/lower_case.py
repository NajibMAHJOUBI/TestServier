
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import Series


def lower_case(series: 'Series') -> 'Series':
    return series.str.lower()
