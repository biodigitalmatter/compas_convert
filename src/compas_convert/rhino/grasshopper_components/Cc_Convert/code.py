"""
Convert compas object to Rhino object.
compas_convert 0.1.3
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ghpythonlib.componentbase import executingcomponent as component

from compas_convert import convert


class ConvertComponent(component):
    def RunScript(self, input):
        output = None
        if input:
            output = convert(input)

        return output
