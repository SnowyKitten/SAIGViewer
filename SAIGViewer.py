from __future__ import unicode_literals
from DataReader import DataReader
import sys
import os
import random
from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
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
            h, w = len(d), len(d[0])
            if h > w:
                aspect = (5/(h/w))
            elif w > h:
                aspect = (5/(w/h))
                
            if style == 'color':
                self.axes.imshow(d, cmap=cmap, vmin=vmin, vmax=vmax,
                                 extent=[ox, ox+len(d[0])*dx, oy+len(d)*dy, oy],
                                 aspect=aspect,
                                 interpolation=interpolation)
                self.draw()
                # returns the height and width of the data matrix
                return len(d), len(d[0])
            
            else:
                # plot wiggle here if desired
                return


class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        self.path = ""
        self.old_xlim = 0
        self.old_ylim = 0
        self.data_dim = 0,0
        self.style = 'color' 
        self.wiggle_fill_color = 'k'
        self.wiggle_line_color = 'k'
        self.wiggle_trace_increment = 1
        self.xcur = 1.2
        self.fignum = 1
        self.cmap = 'RdGy'
        self.vmin = -1
        self.vmax = 1
        self.title = " "
        self.xlabel = " "
        self.xunits = " "
        self.ylabel = " "
        self.yunits = " "
        self.ox = 0
        self.dx = 1
        self.oy = 0
        self.dy = 1
        self.dpi = 100
        self.wbox = 8
        self.hbox = 8
        self.name = None
        self.interpolation = "none"        
        
        
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtGui.QMenu('&File', self)
        
        self.file_menu.addAction('&Open File...', self.openFile, QtCore.Qt.CTRL + QtCore.Qt.Key_O)

        self.file_menu.addAction('&About', self.about, QtCore.Qt.CTRL + QtCore.Qt.Key_A)     
        
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        
        self.menuBar().addMenu(self.file_menu)
        
        
        self.colour_menu = QtGui.QMenu('&Colour Map', self)
        self.colour_menu.addAction('&RdGy', self.setRdGy)
        self.colour_menu.addAction('&Seismic', self.setSeismic)
        self.colour_menu.addAction('&Enter a cmap' , self.setCustom)

        
        self.menuBar().addMenu(self.colour_menu)


        self.main_widget = QtGui.QWidget(self)

        # create widow layout
        l = QtGui.QGridLayout(self.main_widget)
        
        # create an initial image canvas 
        self.sc = MyStaticMplCanvas(self.main_widget, width=4, height=4, dpi=100)
        
        # create a zoom dialog button
        self.zbtn = QtGui.QPushButton('Zoom', self)
        self.zbtn.clicked.connect(self.zoomDialog)
                    
        
        # create the x-axis pan slider
        self.x_sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.x_sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.x_sld.valueChanged[int].connect(self.xChangeValue)   
        self.x_sld.setTickPosition(1)
        self.x_sld.setMinimum(0)
        self.x_sld.setMaximum(100)
        self.x_sld.setTickInterval(4)
        self.x_sld.setRange(0,100)
        self.x_sld.setValue(50)
        
        # create the y-axis pan slider
        self.y_sld = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.y_sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.y_sld.valueChanged[int].connect(self.yChangeValue)
        self.y_sld.setTickPosition(2)
        self.y_sld.setMinimum(0)
        self.y_sld.setMaximum(100)
        self.y_sld.setTickInterval(4)
        self.y_sld.setRange(0,100)         
        self.y_sld.setValue(50)   
        
        # call the default mpl toolbar
        self.mpl_toolbar = NavigationToolbar(self.sc, self.main_widget)
        self.sc.mpl_connect('key_press_event', self.on_key_press)

        # add the separate widgets into the display
        l.addWidget(self.y_sld, 0, 0)
        l.addWidget(self.sc, 0, 1)
        l.addWidget(self.x_sld, 1, 1)
        l.addWidget(self.mpl_toolbar, 2, 1)      
        l.addWidget(self.zbtn, 2,2)
        

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        
        
    def zoomDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Zoom', 'Zoom to Xmin, Xmax, Ymin, Ymax')
        if ok:
            try:
                dim = text.strip().split(',')

                # set slider bars to approximately the correct location given a zoom
                self.y_sld.setValue((self.data_dim[0]//int(dim[3]))*100)
                self.x_sld.setValue((int(dim[0])//self.data_dim[1])*100)
            
                self.sc.axes.set_xlim(int(dim[0]), int(dim[1]))
                self.sc.axes.set_ylim(int(dim[3]), int(dim[2]))
                self.sc.draw()   
            except:
                return

 
      
    
    def xChangeValue(self, value):
        modifier = value - self.old_xlim
        self.old_xlim = value
        # get height and width of data matrix
        ht, wt = self.data_dim[0], self.data_dim[1]
        tickwt = wt/100
        old_min, old_max = self.sc.axes.get_xlim()
        self.sc.axes.set_xlim([old_min+(tickwt*modifier),old_max+(tickwt*modifier)])
        self.sc.draw()
        
        return
    
    def yChangeValue(self, value):
        modifier = value - self.old_ylim
        self.old_ylim = value
        # get height and width of data matrix
        ht, wt = self.data_dim[0], self.data_dim[1]
        tickht = ht/100
        old_min, old_max = self.sc.axes.get_ylim()
        self.sc.axes.set_ylim([old_min+(-1*tickht*modifier),old_max+(-1*tickht*modifier)])
        self.sc.draw()        
        return    

    def on_key_press(self, event):
        #implement something here
        key_press_handler(event, self.sc, self.mpl_toolbar)


    def setCustom(self):
        self.sc.cmap, ok = QtGui.QInputDialog.getText(self, 'Set Cmap', 'Cmap')
        self.sc.compute_figure(file_name = self.path, cmap = self.sc.cmap)
        self.x_sld.setValue(50)
        self.y_sld.setValue(50)  
        

    def setSeismic(self):
        self.sc.cmap = 'seismic'
        self.sc.compute_figure(file_name = self.path, cmap = self.sc.cmap)
        self.x_sld.setValue(50)
        self.y_sld.setValue(50)            
        
    def setRdGy(self):
        self.sc.cmap = 'RdGy'
        self.sc.compute_figure(file_name = self.path, cmap = self.sc.cmap)
        self.x_sld.setValue(50)
        self.y_sld.setValue(50)            


    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()
        
    def openFile(self):
        self.path = QtGui.QFileDialog.getOpenFileName()
        self.data_dim = self.sc.compute_figure(file_name = self.path, cmap = self.cmap)
        self.x_sld.setValue(50)
        self.y_sld.setValue(50)        

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
sys.exit(qApp.exec_())
#qApp.exec_()