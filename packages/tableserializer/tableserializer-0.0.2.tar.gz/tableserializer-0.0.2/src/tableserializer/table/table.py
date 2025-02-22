from typing import Union, List, Dict

import pandas as pd


class Table:

    def __init__(self, table_contents: Union[pd.DataFrame, List[Dict[str, str]], List[List[str]]]):
        if isinstance(table_contents, pd.DataFrame):
            self._table = table_contents
        elif all(isinstance(row, list) for row in table_contents):
            self._table = pd.DataFrame(table_contents[1:], columns=table_contents[0])
        elif all(isinstance(row, dict) for row in table_contents):
            self._table = pd.DataFrame(table_contents)
        else:
            raise TypeError(f'{type(table_contents).__name__} is not a supported table format. Table must be of one '
                            f'of the following types: pandas.DataFrame, List[List[str]], List[Dict[str, str]].')

    def as_list_of_lists(self) -> List[List[str]]:
        return self._table.apply(lambda r: r.tolist(),axis=1).tolist()

    def as_list_of_dicts(self) -> List[Dict[str, str]]:
        return self._table.apply(lambda r: {key: value for key, value in r.items()},axis=1).tolist()

    def as_dataframe(self) -> pd.DataFrame:
        return self._table
