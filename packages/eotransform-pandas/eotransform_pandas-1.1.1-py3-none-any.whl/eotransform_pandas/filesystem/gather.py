from collections import defaultdict, deque
from concurrent.futures.process import ProcessPoolExecutor
from functools import partial
from pathlib import Path
from typing import Dict, Callable, Optional, Sequence, AnyStr, Pattern, Generator

import pandas as pd


def gather_files(root: Path, naming_convention: Callable[[str], Dict],
                 sub_folder_structure: Optional[Sequence[Pattern[AnyStr]]] = None,
                 index: Optional[str] = None,
                 ncores: Optional[int] = 1) -> pd.DataFrame:
    directories = list()
    _add_sub_folders(root, deque(sub_folder_structure or []), directories)
    files = _files_generator(directories)
    process_func = partial(_process_file, naming_convention=naming_convention)
    with ProcessPoolExecutor(max_workers=ncores) as executor:
        files_and_metadata = executor.map(process_func, files)

    data = defaultdict(list)
    for file, meta_data in files_and_metadata:
        if meta_data:
            _add_file_and_meta_data(data, file, meta_data)

    return _make_data_frame_from(data, index)


def _process_file(file, naming_convention):
    return file, naming_convention(file.name)


def _files_generator(directories: list) -> Generator[Path, None, None]:
    for directory in directories:
        for file in directory.iterdir():
            if file.is_file():
                yield file


def _add_sub_folders(current: Path, sub_folders: deque, file_list: list):
    if sub_folders:
        sub_pattern = sub_folders.popleft()
        for directory in current.iterdir():
            if directory.is_dir() and sub_pattern.fullmatch(directory.name):
                _add_sub_folders(directory, deque(sub_folders), file_list)
    else:
        file_list.append(current)


def _make_data_frame_from(data, index):
    df = pd.DataFrame(data)
    if df.empty:
        return df
    if index:
        df.set_index(index, inplace=True)
        df.sort_index(inplace=True)
    return df


def _add_file_and_meta_data(data, file, meta_data):
    data['filepath'].append(file)
    for k, v in meta_data.items():
        data[k].append(v)
