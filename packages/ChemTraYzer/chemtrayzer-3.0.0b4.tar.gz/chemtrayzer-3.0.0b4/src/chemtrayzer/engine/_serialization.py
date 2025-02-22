"""
This module contains the logic for serializing investigations. It can be
considered an implementation detail and should not be used outside of the
engine.
"""

import pickle
from typing import Any, Mapping


class PickyPickler(pickle.Pickler):
    '''
    This pickler only pickles objects that are not in a predefined list of
    objects not to pickle.

    :param file: File to which to write
    :param sep_objs: mapping containing the objects which should not be pickled
                     accessible by their unique names
    '''

    def __init__(self, file, *,
                 sep_objs: Mapping[str, Any] = None, **kwargs) -> None:
        super().__init__(file, **kwargs)

        self._sep_objs = {}

        if sep_objs is not None:
            for name, obj in sep_objs.items():
                if id(obj) in self._sep_objs:
                    raise ValueError('Each object can appear only once in '
                                     'sep_objs.')

                self._sep_objs[id(obj)] = name

    def persistent_id(self, obj: Any) -> str:
        try:
            return self._sep_objs[id(obj)]

        except KeyError: # object should not be pickled
            return None


class PickyUnpickler(pickle.Unpickler):
    '''
    This class should be used to deserialize chemtrayer objects. It replaces
    the ids of separately serializable objects with the objects provided in the
    constructor.

    :param file: file containing the pickled objects
    :param sep_objs: list of separately serializable objects
    '''

    def __init__(self, file, sep_objs: Mapping[str, Any],
            **kwargs) -> None:
        super().__init__(file, **kwargs)

        self._sep_objs = sep_objs

    def persistent_load(self, pid: Any) -> Any:
        try:
            return self._sep_objs[pid]
        except KeyError as err:
            raise pickle.UnpicklingError(f'Expected object with name {pid}, '
                                         'but no such object was supplied to '
                                         'the unpickler.') from err
