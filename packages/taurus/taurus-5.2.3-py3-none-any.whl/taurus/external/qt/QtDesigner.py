# -*- coding: utf-8 -*-
#
# Copyright © 2014-2015 Colin Duquesnoy
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)

"""
Provides QtDesigner classes and functions.
"""

from . import PYQT5, PythonQtError


if PYQT5:
    from PyQt5.QtDesigner import *  # noqa: F403,F401
else:
    raise PythonQtError("No compatible Qt bindings could be found")

del PYQT5, PythonQtError
