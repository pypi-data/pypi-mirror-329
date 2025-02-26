# -*- coding: utf-8 -*-
#
# Copyright © 2014-2015 Colin Duquesnoy
# Copyright © 2009- The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)

"""
Provides QtWebEngineWidgets classes and functions.
"""

from . import PYQT5, PYSIDE2, PythonQtError


if PYQT5:
    from PyQt5.QtWebEngineWidgets import *  # noqa: F403,F401
elif PYSIDE2:
    from PySide2.QtWebEngineWidgets import *  # noqa: F403,F401
else:
    raise PythonQtError("No Qt bindings could be found")
