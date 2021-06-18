from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import glob
import os

import compas.plugins
from compas_ghpython.components import install_userobjects
from compas_ghpython.components import uninstall_userobjects

from compas_convert import PKG_DIR

GH_COMPONENTS_DIR = os.path.join(PKG_DIR, "rhino", "grasshopper_components", "ghuser")


@compas.plugins.plugin(category="install")
def installable_rhino_packages():
    return ["compas_convert"]


@compas.plugins.plugin(category="install")
def after_rhino_install(installed_packages):
    if "compas_convert" not in installed_packages:
        return []

    installed_objects = install_userobjects(GH_COMPONENTS_DIR)

    return [
        (
            "compas_convert",
            "Installed {} GH User Objects".format(len(installed_objects)),
            True,
        )
    ]


@compas.plugins.plugin(category="install")
def after_rhino_uninstall(uninstalled_packages):
    if "compas_convert" not in uninstalled_packages:
        return []

    userobjects = [
        os.path.basename(ghuser)
        for ghuser in glob.glob(os.path.join(GH_COMPONENTS_DIR, "*.ghuser"))
    ]
    uninstalled_objects = uninstall_userobjects(userobjects)

    uninstall_errors = [uo[0] for uo in uninstalled_objects if not uo[1]]
    error_msg = (
        ""
        if not uninstall_errors
        else "and {} failed to uninstall".format(len(uninstall_errors))
    )

    return [
        (
            "compas_convert",
            "Uninstalled {} GH User Objects {}".format(
                len(uninstalled_objects), error_msg
            ),
            True,
        )
    ]
