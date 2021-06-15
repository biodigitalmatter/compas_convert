from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def pytest_ignore_collect(path):
    if "rhino" in str(path):
        return True
