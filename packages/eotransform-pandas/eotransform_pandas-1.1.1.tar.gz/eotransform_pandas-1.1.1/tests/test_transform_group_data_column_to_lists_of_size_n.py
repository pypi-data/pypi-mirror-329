from datetime import datetime

import pandas as pd
import pytest

from assertions import assert_data_frame_eq
from eotransform_pandas.transformers.group_by_n import GroupColumnByN
from factories import make_dataset


def test_group_filepaths():
    file_dataset = make_dataset(index='datetime_1',
                                datetime_1=pd.date_range(datetime(2000, 1, 1), datetime(2000, 1, 6)),
                                filepath=['0.tif', '1.tif', '2.tif', '3.tif', '4.tif', '5.tif'])
    assert_data_frame_eq(GroupColumnByN('filepath', group_size=3)(file_dataset),
                         make_dataset(index='datetime_1',
                                      datetime_1=[datetime(2000, 1, 1), datetime(2000, 1, 4)],
                                      filepaths=[['0.tif', '1.tif', '2.tif'], ['3.tif', '4.tif', '5.tif']]))


def test_error_if_number_of_input_files_is_not_multiple_of_requested_bands():
    file_dataset = make_dataset(index='datetime_1',
                                datetime_1=pd.date_range(datetime(2000, 1, 1), datetime(2000, 1, 5)),
                                filepath=['0.tif', '1.tif', '2.tif', '3.tif', '4.tif'])
    with pytest.raises(GroupColumnByN.NumInputFilesMismatchError):
        GroupColumnByN('filepath', group_size=3)(file_dataset)


def test_append_different_group_suffix():
    file_dataset = make_dataset(index='datetime_1',
                                datetime_1=pd.date_range(datetime(2000, 1, 1), datetime(2000, 1, 6)),
                                measurements=[0, 1, 2, 3, 4, 5])
    assert_data_frame_eq(GroupColumnByN('measurements', group_size=3, group_suffix='_groups')(file_dataset),
                         make_dataset(index='datetime_1',
                                      datetime_1=[datetime(2000, 1, 1), datetime(2000, 1, 4)],
                                      measurements_groups=[[0, 1, 2], [3, 4, 5]]))
