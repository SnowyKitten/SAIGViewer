from __future__ import unicode_literals
from DataReader import DataReader
import sys
import os
import random
from matplotlib.backends import qt4_compat
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

import numpy as np
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import *


progname = "SAIGViewer WIP"
#os.path.basename(sys.argv[0])
progversion = "0.01"


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    def compute_figure(self,file_name="", 
                       style = 'color', 
                       wiggle_fill_color = 'k',
                       wiggle_line_color = 'k',
                       wiggle_trace_increment = 1,
                       xcur = 1.2,
                       fignum = 1,
                       cmap = 'RdGy',
                       aspect = 2,
                       vmin = -1,
                       vmax = 1,
                       title = " ",
                       xlabel = " ",
                       xunits = " ",
                       ylabel = " ",
                       yunits = " ",
                       ox = 0,
                       dx = 1,
                       oy = 0,
                       dy = 1,
                       dpi = 100,
                       wbox = 8,
                       hbox = 8,
                       name = None,
                       interpolation = "none"):
        if file_name == "":
            self.axes.plot()
        else:
            d = dr.read_data(file_name)
            if style == 'color':
                self.axes.imshow(d, cmap=cmap, vmin=vmin, vmax=vmax,
                                 extent=[ox, ox+len(d[0])*dx, oy+len(d)*dy, oy],
                                 aspect=aspect)
                self.draw()
            else:
                # plot wiggle here
                return

            


        

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtGui.QMenu('&File', self)
        
        self.file_menu.addAction('&Open File...', self.openFile, QtCore.Qt.CTRL + QtCore.Qt.Key_O)

        self.file_menu.addAction('&About', self.about, QtCore.Qt.CTRL + QtCore.Qt.Key_A)     
        
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        
        self.menuBar().addMenu(self.file_menu)


        self.main_widget = QtGui.QWidget(self)

        l = QtGui.QGridLayout(self.main_widget)
        self.sc = MyStaticMplCanvas(self.main_widget, width=4, height=4, dpi=100)
        
        y_sld = QtGui.QSlider(QtCore.Qt.Vertical, self)
        y_sld.setFocusPolicy(QtCore.Qt.NoFocus)
        y_sld.valueChanged[int].connect(self.yChangeValue)
        
        x_sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        x_sld.setFocusPolicy(QtCore.Qt.NoFocus)
        x_sld.valueChanged[int].connect(self.xChangeValue)       

        
        
        self.mpl_toolbar = NavigationToolbar(self.sc, self.main_widget)
        self.sc.mpl_connect('key_press_event', self.on_key_press)

        l.addWidget(y_sld, 0, 0)
        l.addWidget(self.sc, 0, 1)
        l.addWidget(x_sld, 1, 1)
        l.addWidget(self.mpl_toolbar, 2, 1)        
        

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        
    def xChangeValue(self, value):
        return
    
    def yChangeValue(self, value):
        return    

    def on_key_press(self, event):
        print('you pressed', event.key)
        #implement something here
        key_press_handler(event, self.sc, self.mpl_toolbar)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()
        
    def openFile(self):
        path = QtGui.QFileDialog.getOpenFileName()
        self.sc.compute_figure(file_name = path)

    def about(self):
        QtGui.QMessageBox.about(self, "About",
"""
Simple Plot Viewer built for SAIG (Signal Analysis and Imaging Group) at the University of Alberta

"""
)

dr = DataReader()
qApp = QtGui.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
#sys.exit(qApp.exec_())
#qApp.exec_()