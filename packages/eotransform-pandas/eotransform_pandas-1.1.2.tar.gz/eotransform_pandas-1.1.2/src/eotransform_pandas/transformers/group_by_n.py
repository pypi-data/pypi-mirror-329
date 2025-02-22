from typing import Optional

from eotransform.protocol.transformer import Transformer
from pandas import DataFrame


class GroupColumnByN(Transformer[DataFrame, DataFrame]):
    class NumInputFilesMismatchError(AssertionError):
        ...

    def __init__(self, column_to_group: str, group_size: int, group_suffix: Optional[str] = 's'):
        self._column_to_group = column_to_group
        self._group_size = group_size
        self._group_suffix = group_suffix

    def __call__(self, x: DataFrame) -> DataFrame:
        if len(x) % self._group_size != 0:
            msg = f"{len(x)} input files is not a multiple of requested group size {self._group_size}"
            raise GroupColumnByN.NumInputFilesMismatchError(msg)

        x['group_n_id'] = [bi for bi in range(0, len(x), self._group_size) for _ in range(self._group_size)]
        groups = x.groupby('group_n_id')[self._column_to_group].apply(list)
        x = x.join(groups, on='group_n_id', how='right', rsuffix=self._group_suffix)
        x.drop_duplicates(['group_n_id'], keep='first', inplace=True)
        x.drop(self._column_to_group, axis=1, inplace=True)
        x.drop('group_n_id', axis=1, inplace=True)
        return x
