#!/usr/bin/env python3

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np


x = np.random.normal(size=1000)
y = np.random.normal(size=1000)
pg.plot(x,y,pen=None,symbol='o',title='first graph')


if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()