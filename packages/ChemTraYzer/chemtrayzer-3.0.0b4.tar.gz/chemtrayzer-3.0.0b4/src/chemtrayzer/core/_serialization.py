'''
Interface defintions needed by the database. These interfaces are in a separate
module to avoid circular imports
'''
from __future__ import annotations

from abc import ABC, abstractmethod

class IJsonConvertible(ABC):
    '''base class/interface for types that can be de-/serialized from/to JSON'''

    @abstractmethod
    def to_json(self) -> str:
        '''returns a JSON-serialized version of this object'''

    @classmethod
    @abstractmethod
    def from_json(cls, json: str) -> IJsonConvertible:
        '''creates an object from its json representation.

        For dataclasses you could use dict2dataclass to implement this.'''
