from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pkgutil

import compas_convert
from compas_convert.universal_converter.type_converter_match import TypeConverterMatch


class UniversalConverter(object):
    def __init__(self):
        self._converters = None
        self._input_type_to_converters_dict = None

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
    def input_type_to_converters_dict(self):
        if not self._input_type_to_converters_dict:
            self._create_input_type_to_converters_dict()

        return self._input_type_to_converters_dict

    def convert(self, obj, input_type_override=None, output_type_override=None):
        """."""
        input_type = input_type_override or type(obj)

        # Get converters for exact type match
        compat_converters = self.input_type_to_converters_dict.get(input_type) or []

        # Get converters where input parent matches
        for type_key, converters in self.input_type_to_converters_dict.items():
            if issubclass(input_type, type_key):
                compat_converters += converters

        try:

            if output_type_override:
                # raises StopIteration if none of the applicable converters
                # has specified to type as output
                converter = next(
                    (
                        conv
                        for conv in compat_converters
                        if conv.output_type == output_type_override
                    )
                )
            else:
                # raises IndexError if applicable converters are zero
                converter = compat_converters[-1]
        except (IndexError, StopIteration):
            raise RuntimeError(
                "Could not convert object of type {} ".format(type(obj))
                + "(constraint input: {}, constraint output: {})".format(
                    input_type_override, output_type_override
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

    def _create_input_type_to_converters_dict(self):
        def yield_available_input_types():
            for conv in self.converters:
                for input_type in conv.input_types:
                    yield input_type

        self._input_type_to_converters_dict = {}

        for type_ in yield_available_input_types():
            # Check that is that is hasn't already been added
            if type_ not in self._input_type_to_converters_dict.keys():
                matches = [
                    TypeConverterMatch(c, input_type=type_) for c in self.converters
                ]
                valid_matches = [
                    match for match in matches if match.is_input_type_match()
                ]
                valid_matches.sort(reverse=True)

                self._input_type_to_converters_dict[type_] = [
                    match.func for match in valid_matches
                ]

    def _print_input_type_converter_mapping(self):
        string = ""

        for key, value in self.input_type_to_converters_dict.items():
            string += "{}: {}\n".format(key, ",\n\t".join([str(c) for c in value]))

        print(string)


# Everything is loaded lazily so this shouldn't cost anything
UNIVERSAL_CONVERTER = UniversalConverter()


def convert(obj, input_type_override=None, output_type=None):
    """Convert CAD native object to COMPAS object, or vice versa."""
    return UNIVERSAL_CONVERTER.convert(
        obj, input_type_override=input_type_override, output_type_override=output_type
    )
