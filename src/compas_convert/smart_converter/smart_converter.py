from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pkgutil

import compas_convert
from compas_convert.smart_converter.type_converter_match import TypeConverterMatch


class SmartConverter(object):
    def __init__(self):
        self._converters = None
        self._from_type_converter_mapping = None

    def __str__(self):
        string = "SmartConverter("
        if not self._converters:
            string += "No loaded converter functions)"
        else:
            string += (
                "Loaded converter functions: "
                + ",\n".join([str(c) for c in self._converters])
                + ")"
            )
        return string

    @property
    def converters(self):
        if not self._converters:
            self._create_converter_list()

        return self._converters

    @property
    def from_type_converter_mapping(self):
        if not self._from_type_converter_mapping:
            self._create_from_converter_mapping()

        return self._from_type_converter_mapping

    def convert(self, obj, from_type=None, to_type=None):
        """."""
        _from = from_type or type(obj)

        # Get converters for exact type match
        compat_converters = self.from_type_converter_mapping.get(_from) or []

        # Get converters where input parent matches
        for type_key, converters in self.from_type_converter_mapping.items():
            if issubclass(_from, type_key):
                compat_converters += converters

        try:

            if to_type:
                # raises StopIteration if none of the applicable converters
                # has specified to type as output
                converter = next(
                    (conv for conv in compat_converters if conv.to == to_type)
                )
            else:
                # raises IndexError if applicable converters are zero
                converter = compat_converters[-1]
        except (IndexError, StopIteration):
            raise RuntimeError(
                "Could not convert object of type {} ".format(type(obj))
                + "(constraint input: {}, constraint output: {})".format(
                    from_type, to_type
                )
            )

        return converter(obj)

    def _create_converter_list(self):
        def _try_import_internal(module_name, from_module=None):
            pkg_path = "compas_convert."

            if from_module:
                pkg_path += "{}.".format(from_module)

            try:
                return __import__(
                    pkg_path + module_name, fromlist=["__name__"], level=0
                )
            except ImportError:
                return

        modules = [
            module_name
            for _, module_name, is_pkg in pkgutil.iter_modules(compas_convert.__path__)
            if is_pkg
        ]

        self._converters = []
        for module_name in modules:
            module = _try_import_internal(module_name)
            if module:
                # for obj_name in __all__ if __all__ exists
                for obj_name in getattr(module, "__all__", []):
                    obj = getattr(module, obj_name)
                    if getattr(obj, "is_converter", False):
                        self._converters.append(obj)

    def _create_from_converter_mapping(self):
        def yield_available_from_types():
            for conv in self.converters:
                for from_type in conv.from_:
                    yield from_type

        self._from_type_converter_mapping = {}

        for type_ in yield_available_from_types():
            # Check that is that is hasn't already been added
            if type_ not in self._from_type_converter_mapping.keys():
                matches = [TypeConverterMatch(c, from_=type_) for c in self.converters]
                valid_matches = [
                    match for match in matches if match.is_from_type_match()
                ]
                valid_matches.sort(reverse=True)

                self._from_type_converter_mapping[type_] = [
                    match.func for match in valid_matches
                ]

    def _print_input_type_converter_mapping(self):
        string = ""

        for key, value in self.from_type_converter_mapping.items():
            string += "{}: {}\n".format(key, ",\n\t".join([str(c) for c in value]))

        print(string)


# Everything is loaded lazily so this shouldn't cost anything
SMART_CONVERTER = SmartConverter()


def convert(obj, from_=None, to=None):
    # print(SMART_CONVERTER)
    # print(SMART_CONVERTER._print_input_type_converter_mapping())
    return SMART_CONVERTER.convert(obj, from_type=from_, to_type=to)
