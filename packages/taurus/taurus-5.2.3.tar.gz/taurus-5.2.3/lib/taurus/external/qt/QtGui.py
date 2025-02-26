# -*- coding: utf-8 -*-
#
# Copyright © 2018- CELLS / ALBA Synchrotron, Bellaterra, Spain
# Copyright © 2014-2015 Colin Duquesnoy
# Copyright © 2009-2018 The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)

"""
Provides QtGui classes and functions.
.. warning:: Contrary to qtpy.QtGui, this module exposes the namespace
    available in ``PyQt4.QtGui``.
"""

from . import PYQT5, PYSIDE2, PythonQtError


if PYQT5:
    from PyQt5.QtGui import *  # noqa: F403,F401

    # import * from QtWidgets and QtPrintSupport for PyQt4 style compat
    from PyQt5.QtWidgets import *  # noqa: F403,F401
    from PyQt5.QtPrintSupport import *  # noqa: F403,F401
elif PYSIDE2:
    from PySide2.QtGui import *  # noqa: F403,F401

    # import * from QtWidgets and QtPrintSupport for PyQt4 style compat
    from PySide2.QtWidgets import *  # noqa: F403,F401
    from PySide2.QtPrintSupport import *  # noqa: F403,F401
else:
    raise PythonQtError("No Qt bindings could be found")
