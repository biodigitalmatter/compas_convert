# compas_convert

![Build and test](https://github.com/biodigitalmatter/compas_convert/actions/workflows/test-build-docs-release.yaml/badge.svg)
[![PyPI Package latest release](https://img.shields.io/pypi/v/compas-convert.svg)](https://pypi.org/project/compas-convert)
[![Conda](https://img.shields.io/conda/v/conda-forge/compas_convert)](https://anaconda.org/conda-forge/compas_convert)
![License](https://img.shields.io/github/license/biodigitalmatter/compas_convert)

Conversions of [COMPAS](https://compas.dev) geometry objects to CAD specific objects.

## Supported CAD environments

* [Rhino/Grasshopper](https://www.rhino3d.com/)
* Blender (planned)

## Installation

```bash
pip install compas_convert
python -m compas_rhino.install
```

This will install the package into your Rhino environment and add a grasshopper
component next to the COMPAS package's components.

## Documentation

The function `convert` which you can import from the top level of the package
(`from compas_convert import convert`) will convert compas object to CAD object
or CAD object to compas object. It does this based on the environment and the
input object.

You can also use normal converter functions:

```python
from compas.geometry import Point
from compas_convert.rhino import point_to_rhino_point

compas_pt = Point(10, 10, 0)
rhino_pt = point_to_rhino_pt(compas_pt)
```

### Under the hood

Converter functions can be found in subpackages named after the CAD software it
converts to and from. The modules are named `compas_to_*` and `*_to_compas`. The
convert functions are decorated with the decorator
`compas_convert.register_converter` where possible input types are specified and
the output type.

This metadata is used by the function `compas_convert.convert` which on its
first use maps types and converters and uses that mapping to convert object
without the need to specify either input type or output type. Input type or
output type can however be specified to override the default.

## Conversion diagrams

![Conversions](./docs/conversion_diagram.svg)
