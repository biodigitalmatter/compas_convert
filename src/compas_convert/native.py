from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.data

from compas_convert import register_converter


@register_converter([str], compas.data.Data)
def json_str_to_compas_obj(json_str):  # type: (str) -> compas.data.Data
    """Convert JSON string to object based on :class:`compas.data.Data`."""
    return compas.data.json_loads(json_str)


def compas_obj_to_json_str(obj, pretty=False):  # type: (compas.Base, bool) -> str
    """Convert object based on :class:`compas.data.Data` to JSON string.

    Just use the native function instead.
    """
    return compas.data.json_dumps(obj, pretty=pretty)
