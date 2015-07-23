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
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
    def compute_figure(self,file_name=""):
        if file_name == "":
            self.axes.plot()
        else:
            d = dr.read_data(file_name)
            self.axes.imshow(d)
            self.draw()
            
    #def update_figure(


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

        l = QtGui.QVBoxLayout(self.main_widget)
        self.sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(self.sc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)


    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()
        
    def openFile(self):
        path = QtGui.QFileDialog.getOpenFileName()
        self.sc.compute_figure(path)    

    def about(self):
        QtGui.QMessageBox.about(self, "About",
"""
Simple Plot Viewer built for SAIG (Signal Analysis and Imaging Group) at the University of Alberta

Developer: Randy Wong
"""
)

dr = DataReader()
qApp = QtGui.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
#sys.exit(qApp.exec_())
#qApp.exec_()