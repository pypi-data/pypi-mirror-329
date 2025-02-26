# -*- coding: utf-8 -*-
#
# Copyright © 2009- The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)

"""QtHelp Wrapper.
"""

from . import PYQT5
from . import PYSIDE2

if PYQT5:
    from PyQt5.QtHelp import *  # noqa: F403,F401
elif PYSIDE2:
    from PySide2.QtHelp import *  # noqa: F403,F401

del PYQT5, PYSIDE2
