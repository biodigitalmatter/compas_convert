from compas_convert import register_converter

import compas.data


@register_converter(from_=[str], to=[compas.data.Data])
def json_str_to_compas_obj(json_str):  # type: (str) -> compas.data.Data
    """Convert JSON string to object based on :class:`compas.data.Data`."""
    return compas.data.json_loads(json_str)


def compas_obj_to_json_str(obj, pretty=False):  # type: (compas.Base, bool) -> str
    """Convert object based on :class:`compas.data.Data` to JSON string.

    Just use the native function instead.
    """
    return compas.data.json_dumps(obj, pretty=pretty)
