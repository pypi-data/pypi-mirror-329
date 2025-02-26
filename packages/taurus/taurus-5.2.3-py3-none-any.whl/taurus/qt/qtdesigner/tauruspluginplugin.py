#!/usr/bin/env python

# ###########################################################################
#
# This file is part of Taurus
#
# http://taurus-scada.org
#
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Taurus is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Taurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
#
# ###########################################################################

"""
Plugin module for QtDesigner that auto generates a the collections of plugins
to be added to the Qt designer catalog
"""

from taurus.external.qt import QtDesigner
from importlib import import_module


_DEFAULT_TAURUS_WIDGET_CATALOG = [
    "taurus.qt.qtgui.button:TaurusCommandButton",
    "taurus.qt.qtgui.button:TaurusLauncherButton",
    "taurus.qt.qtgui.button:TaurusLockButton",
    "taurus.qt.qtgui.compact:TaurusBoolRW",
    "taurus.qt.qtgui.compact:TaurusLabelEditRW",
    "taurus.qt.qtgui.compact:TaurusReadWriteSwitcher",
    "taurus.qt.qtgui.container:TaurusFrame",
    "taurus.qt.qtgui.container:TaurusGroupBox",
    "taurus.qt.qtgui.container:TaurusScrollArea",
    "taurus.qt.qtgui.container:TaurusWidget",
    "taurus.qt.qtgui.display:QLed",
    "taurus.qt.qtgui.display:QPixmapWidget",
    "taurus.qt.qtgui.display:TaurusLCD",
    "taurus.qt.qtgui.display:TaurusLabel",
    "taurus.qt.qtgui.display:TaurusLed",
    "taurus.qt.qtgui.extra_guiqwt:TaurusImageDialog",
    "taurus.qt.qtgui.extra_guiqwt:TaurusTrend2DDialog",
    "taurus.qt.qtgui.extra_nexus:TaurusNeXusBrowser",
    "taurus.qt.qtgui.graphic.jdraw:TaurusJDrawSynopticsView",
    "taurus.qt.qtgui.graphic:TaurusGraphicsView",
    "taurus.qt.qtgui.help:AboutDialog",
    "taurus.qt.qtgui.help:HelpPanel",
    "taurus.qt.qtgui.input:GraphicalChoiceWidget",
    "taurus.qt.qtgui.input:TaurusAttrListComboBox",
    "taurus.qt.qtgui.input:TaurusValueCheckBox",
    "taurus.qt.qtgui.input:TaurusValueComboBox",
    "taurus.qt.qtgui.input:TaurusValueLineEdit",
    "taurus.qt.qtgui.input:TaurusValueSpinBox",
    "taurus.qt.qtgui.input:TaurusWheelEdit",
    "taurus.qt.qtgui.panel:DefaultReadWidgetLabel",
    "taurus.qt.qtgui.panel:TangoConfigLineEdit",
    "taurus.qt.qtgui.panel:TaurusAttrForm",
    "taurus.qt.qtgui.panel:TaurusCommandsForm",
    "taurus.qt.qtgui.panel:TaurusForm",
    "taurus.qt.qtgui.panel:TaurusModelChooser",
    "taurus.qt.qtgui.panel:TaurusModelList",
    "taurus.qt.qtgui.panel:TaurusModelSelectorTree",
    "taurus.qt.qtgui.table:QLoggingWidget",
    "taurus.qt.qtgui.table:TaurusDbTableWidget",
    "taurus.qt.qtgui.table:TaurusGrid",
    "taurus.qt.qtgui.table:TaurusPropTable",
    "taurus.qt.qtgui.table:TaurusValuesTable",
    "taurus.qt.qtgui.tree:TaurusDbTreeWidget",
]

_plugins = {}


def build_qtdesigner_widget_plugin(klass):
    from taurus.qt.qtdesigner.taurusplugin import taurusplugin

    class Plugin(taurusplugin.TaurusWidgetPlugin):
        WidgetClass = klass

    Plugin.__name__ = klass.__name__ + "QtDesignerPlugin"
    return Plugin


def _create_plugins():
    from taurus import Logger

    Logger.setLogLevel(Logger.Debug)
    _log = Logger(__name__)

    ok = 0

    # use explicit list of specs instead of original approach of instrospecting
    # with TaurusWidgetFactory().getWidgetClasses()
    # TODO: complement specs with an entry-point
    specs = _DEFAULT_TAURUS_WIDGET_CATALOG
    for spec in specs:
        spec = spec.strip()
        msg = spec + " : "
        try:
            assert ":" in spec, "expected 'modname:classname'"
            _mod_name, _cls_name = spec.rsplit(":", maxsplit=1)
            widget_class = getattr(import_module(_mod_name), _cls_name)
        except Exception as e:
            _log.warning(msg + "error importing: %s", e)
            continue

        try:
            qt_info = widget_class.getQtDesignerPluginInfo()
            assert qt_info is not None, "getQtDesignerPluginInfo() -> None"
            assert "module" in qt_info, "'module' key not available"
        except Exception as e:
            _log.warning(msg + "error getting plugin info: %s", e)
            continue

        try:
            # dynamically create taurus plugin classes and expose them
            plugin_class = build_qtdesigner_widget_plugin(widget_class)
            plugin_class_name = plugin_class.__name__
            globals()[plugin_class_name] = plugin_class
            _plugins[plugin_class_name] = plugin_class
        except Exception as e:
            _log.warning(msg + "error creating plugin: %s", e)
            continue

        # if we got here, everything went fine for this
        _log.info(msg + "ok")
        ok += 1
    _log.info("Designer plugins: %d created, %d failed", ok, len(specs) - ok)


def main():
    try:
        _create_plugins()
    except Exception:
        import traceback

        traceback.print_exc()


class TaurusWidgets(QtDesigner.QPyDesignerCustomWidgetCollectionPlugin):
    def __init__(self, parent=None):
        QtDesigner.QPyDesignerCustomWidgetCollectionPlugin.__init__(parent)
        self._widgets = None

    def customWidgets(self):
        if self._widgets is None:
            self._widgets = [w(self) for w in _plugins.values()]
        return self._widgets


if __name__ != "__main__":
    main()
