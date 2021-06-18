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
    def __init__(self, func, input_type=None, output_type=None):
        self.func = func
        self.input_type = self.ensure_type_obj(input_type)
        self.output_type = self.ensure_type_obj(output_type)

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __repr__(self):
        string = "TypeConverterMatch(Function: {},".format(self.func)
        string += "input_type: {}, output_type: {}, is_match: {}, value: {}".format(
            self.input_type, self.output_type, self.is_match(), self.value
        )

        return string

    @staticmethod
    def _try_return_idx(item, list_, default=None):
        if not item or item not in list_:
            return default

        return list_.index(item)

    @property
    def value(self):  # type: ()  -> Tuple[int, bool]
        return (self._get_input_score(), self._get_output_score())

    def _get_input_score(self):  # type: () -> int
        try:
            return self.func.input_types.index(self.input_type) + 1
        except ValueError:
            return 0

    def _get_output_score(self):  # type: () -> bool
        return self.output_type == self.func.output_type

    def is_match(self):  # type: () -> bool
        return self.is_input_type_match() and self.is_output_type_match()

    def is_input_type_match(self):  # type: () -> bool
        return self.value[0] > 0

    def is_output_type_match(self):  # type: () -> bool
        return self.value[1]

    @staticmethod
    def ensure_type_obj(obj):  # type: (Any) -> Optional[type]
        if obj:
            return obj if isinstance(obj, type) else type(obj)
        else:
            return None
