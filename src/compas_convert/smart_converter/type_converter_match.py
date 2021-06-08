from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from typing import Any
    from typing import Optional
    from typing import Tuple
except ImportError:
    pass


class TypeConverterMatch(object):
    def __init__(self, func, from_=None, to=None):
        self.func = func
        self.from_ = self.ensure_type_obj(from_)
        self.to = self.ensure_type_obj(to)

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __repr__(self):
        string = "TypeConverterMatch(Function: {},".format(self.func)
        string += "from_type: {}, to_type: {}, is_match: {}, value: {}".format(
            self.from_, self.to, self.is_match(), self.value
        )

        return string

    @staticmethod
    def _try_return_idx(item, list_, default=None):
        if not item or item not in list_:
            return default

        return list_.index(item)

    @property
    def value(self):  # type: ()  -> Tuple[int, bool]
        return (self._get_from_score(), self._get_to_score())

    def _get_from_score(self):  # type: () -> int
        try:
            return self.func.from_.index(self.from_) + 1
        except ValueError:
            return 0

    def _get_to_score(self):  # type: () -> bool
        return self.to == self.func.to

    def is_match(self):  # type: () -> bool
        return self.is_from_type_match() and self.is_to_type_match()

    def is_from_type_match(self):  # type: () -> bool
        return self.value[0] > 0

    def is_to_type_match(self):  # type: () -> bool
        return self.value[1]

    @staticmethod
    def ensure_type_obj(obj):  # type: (Any) -> Optional[type]
        if obj:
            return obj if isinstance(obj, type) else type(obj)
        else:
            return None
