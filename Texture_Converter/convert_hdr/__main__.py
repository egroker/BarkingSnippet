#!usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from Qt import QtWidgets

from convert_hdr import ConvertHdr
from misc.painter.get_set_palette_data import set_dark_maya_2016


app = QtWidgets.QApplication.instance()
if not app:
    app = QtWidgets.QApplication(sys.argv)

main_window = ConvertHdr()
set_dark_maya_2016()
main_window.setMinimumSize(5,5)
main_window.resize(600,450)
main_window.show()
app.exec_()
