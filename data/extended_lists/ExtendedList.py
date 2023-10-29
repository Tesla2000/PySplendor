from abc import ABC
from dataclasses import dataclass, fields


@dataclass
class ExtendedList(ABC):

    def __iter__(self):
        return self._list_field.__iter__()

    def __len__(self):
        return self._list_field.__len__()

    def __getitem__(self, item):
        return self._list_field.__getitem__(item)

    def __setitem__(self, key, value):
        return self._list_field.__setitem__(key, value)

    def __getattr__(self, item):
        return getattr(self._list_field, item)

    @property
    def _list_field(self) -> list:
        return getattr(self, next(field.name for field in fields(self) if str(field.type).startswith('list') or field.type == list))
