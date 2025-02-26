# -*- coding: utf-8 -*-
#
# Copyright © 2014-2015 Colin Duquesnoy
# Copyright © 2009- The Spyder Developmet Team
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)

"""
Provides widget classes and functions.
.. warning:: Only PyQt4/PySide QtGui classes compatible with PyQt5.QtWidgets
    are exposed here. Therefore, you need to treat/use this package as if it
    were the ``PyQt5.QtWidgets`` module.
"""

from . import PYQT5, PYSIDE2, PythonQtError
import taurus.core.util.log as __log  # noqa: F401

if PYQT5:
    from PyQt5.QtWidgets import *  # noqa: F403,F401
elif PYSIDE2:
    from PySide2.QtWidgets import *  # noqa: F403,F401
else:
    raise PythonQtError("No Qt bindings could be found")
