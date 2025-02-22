"""For general functions to name, move, copy, ... files and directories
"""
# IF YOU WANT TO ADD A FUNCTION HERE, PLEASE FIRST CONSIDER, IF THERE IS NOT
# A MORE SPECIFIC MODULE OR IF YOU SHOULD CREATE A MORE SPECIFIC MODULE
from __future__ import annotations

import os
from pathlib import Path


def unique_file(path: os.PathLike|str) -> Path:
    """Ensure that the file does not exist by adding a number to the filename.

    For example, if 'file.txt' already exists, the function will return
    'file.001.txt'. If 'file.001.txt' exists, it will return 'file.002.txt',
    and so on. The first free filename will be returned.
    More examples:

    - 'file' -> 'file.001' -> 'file.002'
    - 'file.tar.gz' -> 'file.001.tar.gz' -> 'file.002.tar.gz'
    - 'file.001.txt' -> 'file.001.001.txt' -> 'file.002.001.txt'

    :param path: Path to the file
    """
    path = Path(path)
    if '.' in path.name:
        base, suffixes = path.name.split('.', maxsplit=1)
        suffixes = '.' + suffixes
    else:
        base, suffixes = path.name, ''
    file_nr = 1

    while(path.exists()):
        path = path.with_name(f'{base}.{file_nr:03d}{suffixes}')
        file_nr += 1

        # sanity check
        if file_nr > 5:# 999:
            raise RuntimeError('Too many files with the same name.')

    return path