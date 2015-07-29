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


progname = "SAIGViewer V0.1"
#os.path.basename(sys.argv[0])
progversion = "0.1"


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


# allow attributes to be taken incase in the future we need them
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
        # if first startup, draw an empty plot
        if file_name == "":
            self.axes.plot()
        else:
            # read the .seisd file
            d = dr.read_data(file_name)
            # get the dimensions of the data to help set aspect ratio
            # approximately make it 5:1 in whichever way works better
            h, w = len(d), len(d[0])
            if h > w:
                aspect = (5/(h/w))
            elif w > h:
                aspect = (5/(w/h))
                
            # can enter style later maybe? colour vs wiggle
            if style == 'color':
                # options if needed, otherwise they default to the presets from before
                self.axes.imshow(d, cmap=cmap, vmin=vmin, vmax=vmax,
                                 extent=[ox, ox+len(d[0])*dx, oy+len(d)*dy, oy],
                                 aspect=aspect,
                                 interpolation=interpolation)
                self.draw()
                # returns the width and height [x,y]
                return len(d[0]), len(d)
            
            else:
                # plot wiggle here if desired
                return


class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        self.path = ""
        self.old_xlim = 0
        self.old_ylim = 0
        self.x_sld_max = 100
        self.y_sld_max = 100
        self.data_dim = 0,0
        self.window_dim = 0,0
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
        
        app_icon = QtGui.QIcon()
        app_icon.addFile('Icons/SAIG16x16.png', QtCore.QSize(16,16))
        app_icon.addFile('Icons/SAIG24x24.png', QtCore.QSize(24,24))
        app_icon.addFile('Icons/SAIG32x32.png', QtCore.QSize(32,32))
        app_icon.addFile('Icons/SAIG48x48.png', QtCore.QSize(48,48))
        app_icon.addFile('Icons/SAIG256x256.png', QtCore.QSize(256,256))        
        self.setWindowIcon(app_icon)      
        
        self.main_widget = QtGui.QWidget(self)

        # create widow layout
        l = QtGui.QGridLayout(self.main_widget)
        
        # create an initial image canvas 
        self.sc = MyStaticMplCanvas(self.main_widget, width=4, height=4, dpi=100)
        
        # create a zoom dialog button
        self.zbtn = QtGui.QPushButton('Zoom', self)
        self.zbtn.clicked.connect(self.zoomDialog)
        
        # create a reset button
        self.rbtn = QtGui.QPushButton('Reset', self)
        self.rbtn.clicked.connect(self.resetButton)
                    
        
        # create the x-axis pan slider
        self.x_sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.x_sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.x_sld.valueChanged[int].connect(self.xChangeValue)   
        self.x_sld.setTickPosition(1)
        self.x_sld.setMinimum(0)
        self.x_sld.setMaximum(self.x_sld_max)
        self.x_sld.setTickInterval(4)
        self.x_sld.setRange(0,self.x_sld_max)
        self.x_sld.setValue(self.x_sld_max//2)
        
        # create the y-axis pan slider
        self.y_sld = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.y_sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.y_sld.valueChanged[int].connect(self.yChangeValue)
        self.y_sld.setTickPosition(2)
        self.y_sld.setMinimum(0)
        self.y_sld.setMaximum(self.y_sld_max)
        self.y_sld.setTickInterval(4)
        self.y_sld.setRange(0,self.y_sld_max)         
        self.y_sld.setValue(self.y_sld_max//2)   
        

        # add the separate widgets into the display
        l.addWidget(self.y_sld, 0, 0)
        l.addWidget(self.sc, 0, 1)
        l.addWidget(self.x_sld, 1, 1)     
        l.addWidget(self.zbtn, 2,2)
        l.addWidget(self.rbtn, 1,2)
        
        
        # add all the menu options
        self.file_menu = QtGui.QMenu('&File', self)
        
        self.file_menu.addAction('&Open File...', self.openFile, QtCore.Qt.CTRL + QtCore.Qt.Key_O)

        self.file_menu.addAction('&About', self.about, QtCore.Qt.CTRL + QtCore.Qt.Key_A)     
        
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        
        self.menuBar().addMenu(self.file_menu)
        
        
        self.colour_menu = QtGui.QMenu('&Colour Map', self)
        
        self.seqcmap_menu = QtGui.QMenu('&Sequential', self)
        self.seqcmap2_menu = QtGui.QMenu('&Sequential (2)', self)
        self.divcmap_menu = QtGui.QMenu('&Diverging', self)
        self.qualcmap_menu = QtGui.QMenu('&Qualitative', self)
        self.misccmap_menu = QtGui.QMenu('&Miscellaneous', self)
        
        self.colour_menu.addMenu(self.seqcmap_menu)
        self.colour_menu.addMenu(self.seqcmap2_menu)
        self.colour_menu.addMenu(self.divcmap_menu)
        self.colour_menu.addMenu(self.qualcmap_menu)
        self.colour_menu.addMenu(self.misccmap_menu)
                                
        self.seqcmap_menu.addAction('&Blues', lambda: self.setCmap('Blues'))
        self.seqcmap_menu.addAction('&BuGn', lambda: self.setCmap('BuGn'))
        self.seqcmap_menu.addAction('&BuPu', lambda: self.setCmap('BuPu'))
        self.seqcmap_menu.addAction('&GnBu', lambda: self.setCmap('GnBu'))
        self.seqcmap_menu.addAction('&Greens', lambda: self.setCmap('Greens'))                        
        self.seqcmap_menu.addAction('&Greys', lambda: self.setCmap('Greys'))        
        self.seqcmap_menu.addAction('&Oranges', lambda: self.setCmap('Oranges'))
        self.seqcmap_menu.addAction('&OrRd', lambda: self.setCmap('OrRd'))        
        self.seqcmap_menu.addAction('&PuBu', lambda: self.setCmap('PuBu'))
        self.seqcmap_menu.addAction('&PuBuGn', lambda: self.setCmap('PuBuGn'))
        self.seqcmap_menu.addAction('&PuRd', lambda: self.setCmap('PuRd'))
        self.seqcmap_menu.addAction('&Purples', lambda: self.setCmap('Purples'))
        self.seqcmap_menu.addAction('&RdPu', lambda: self.setCmap('RdPu'))        
        self.seqcmap_menu.addAction('&Reds', lambda: self.setCmap('Reds'))        
        self.seqcmap_menu.addAction('&YlGnBu', lambda: self.setCmap('YlGnBu'))
        self.seqcmap_menu.addAction('&YlOrBr', lambda: self.setCmap('YlOrBr'))        
        self.seqcmap_menu.addAction('&YlOrRd', lambda: self.setCmap('YlOrRd'))
        
        self.seqcmap2_menu.addAction('&afmhot', lambda: self.setCmap('afmhot'))
        self.seqcmap2_menu.addAction('&autumn', lambda: self.setCmap('autumn'))
        self.seqcmap2_menu.addAction('&bone', lambda: self.setCmap('bone'))
        self.seqcmap2_menu.addAction('&cool', lambda: self.setCmap('cool'))
        self.seqcmap2_menu.addAction('&copper', lambda: self.setCmap('copper'))
        self.seqcmap2_menu.addAction('&gist_heat', lambda: self.setCmap('gist_heat'))
        self.seqcmap2_menu.addAction('&gray', lambda: self.setCmap('gray'))
        self.seqcmap2_menu.addAction('&hot', lambda: self.setCmap('hot'))
        self.seqcmap2_menu.addAction('&pink', lambda: self.setCmap('pink'))
        self.seqcmap2_menu.addAction('&spring', lambda: self.setCmap('spring'))
        self.seqcmap2_menu.addAction('&summer', lambda: self.setCmap('summer'))
        self.seqcmap2_menu.addAction('&winter', lambda: self.setCmap('winter'))
        
        self.divcmap_menu.addAction('&BrBG', lambda: self.setCmap('BrBG'))
        self.divcmap_menu.addAction('&bwr', lambda: self.setCmap('bwr'))
        self.divcmap_menu.addAction('&coolwarm', lambda: self.setCmap('coolwarm'))
        self.divcmap_menu.addAction('&PiYG', lambda: self.setCmap('PiYG'))
        self.divcmap_menu.addAction('&PRGn', lambda: self.setCmap('PRGn'))
        self.divcmap_menu.addAction('&PuOr', lambda: self.setCmap('PuOr'))
        self.divcmap_menu.addAction('&RdBu', lambda: self.setCmap('RdBu'))
        self.divcmap_menu.addAction('&RdGy', lambda: self.setCmap('RdGy'))
        self.divcmap_menu.addAction('&RdYlBu', lambda: self.setCmap('RdYlBu'))
        self.divcmap_menu.addAction('&RdYlGn', lambda: self.setCmap('RdYlGn'))
        self.divcmap_menu.addAction('&Spectral', lambda: self.setCmap('Spectral'))
        self.divcmap_menu.addAction('&seismic', lambda: self.setCmap('seismic'))
        
        self.qualcmap_menu.addAction('&Accent', lambda: self.setCmap('Accent'))
        self.qualcmap_menu.addAction('&Dark2', lambda: self.setCmap('Dark2'))
        self.qualcmap_menu.addAction('&Paired', lambda: self.setCmap('Paired'))
        self.qualcmap_menu.addAction('&Pastel1', lambda: self.setCmap('Pastel1'))
        self.qualcmap_menu.addAction('&Pastel2', lambda: self.setCmap('Pastel2'))
        self.qualcmap_menu.addAction('&Set1', lambda: self.setCmap('Set1'))
        self.qualcmap_menu.addAction('&Set2', lambda: self.setCmap('Set2'))
        self.qualcmap_menu.addAction('&Set3', lambda: self.setCmap('Set3'))
        
        self.misccmap_menu.addAction('&gist_earth', lambda: self.setCmap('gist_earth'))
        self.misccmap_menu.addAction('&terrain', lambda: self.setCmap('terrain'))
        self.misccmap_menu.addAction('&ocean', lambda: self.setCmap('ocean'))
        self.misccmap_menu.addAction('&gist_stern', lambda: self.setCmap('gist_stern'))
        self.misccmap_menu.addAction('&brg', lambda: self.setCmap('brg'))
        self.misccmap_menu.addAction('&CMRmap', lambda: self.setCmap('CMRmap'))
        self.misccmap_menu.addAction('&cubehelix', lambda: self.setCmap('cubehelix'))
        self.misccmap_menu.addAction('&gnuplot', lambda: self.setCmap('gnuplot'))
        self.misccmap_menu.addAction('&gnuplo2', lambda: self.setCmap('gnuplot2'))
        self.misccmap_menu.addAction('&gist_ncar', lambda: self.setCmap('gist_ncar'))
        self.misccmap_menu.addAction('&nipy_spectral', lambda: self.setCmap('nipy_spectral'))
        self.misccmap_menu.addAction('&jet', lambda: self.setCmap('jet'))
        self.misccmap_menu.addAction('&rainbow', lambda: self.setCmap('rainbow'))
        self.misccmap_menu.addAction('&gist_rainbow', lambda: self.setCmap('gist_rainbow'))
        self.misccmap_menu.addAction('&hsv', lambda: self.setCmap('hsv'))
        self.misccmap_menu.addAction('&flag', lambda: self.setCmap('flag'))
        self.misccmap_menu.addAction('&prism', lambda: self.setCmap('prism'))
        

        self.colour_menu.addAction('&Enter a cmap' , self.setCustom)

        
        self.menuBar().addMenu(self.colour_menu)        

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        
        
    # resets the display to before zooms
    
    def resetButton(self):
        # set sliders to have no values again
        self.x_sld.setMaximum(0)        
        self.y_sld.setMaximum(0)
        self.x_sld.setValue(0)
        self.y_sld.setValue(0)
        
        self.sc.axes.set_xlim(0, self.x_sld_max)
        self.sc.axes.set_ylim(0, self.y_sld_max)
        self.sc.draw()
        
        return
        
    # opens a dialog window where you type ints [a,b,c,d] with the commas to give
    # Xmin, Xmax, Ymin, and Ymax of the zoomed window
    def zoomDialog(self):
        
        text, ok = QtGui.QInputDialog.getText(self, 'Zoom', 'Zoom to [Xmin, Xmax, Ymin, Ymax]')
        if ok:
            try:
                self.window_dim = text.strip().split(',')
                # change the slider bars so that you can move the slider, but not past the edges
                self.x_sld.setMaximum(self.data_dim[0] - (int(self.window_dim[1]) - int(self.window_dim[0])))        
                self.y_sld.setMaximum(self.data_dim[1] - (int(self.window_dim[3]) - int(self.window_dim[2])))               
                
                # set slider bars to approximately the correct location given a zoom            
                self.y_sld.setValue(self.y_sld_max - int(self.window_dim[3]))
                self.x_sld.setValue(int(self.window_dim[0]))
            
                self.sc.axes.set_xlim(int(self.window_dim[0]), int(self.window_dim[1]))
                self.sc.axes.set_ylim(int(self.window_dim[3]), int(self.window_dim[2]))
                self.sc.draw()
            except:
                # no real exception handling, just do nothing
                return
            
    # called by the x slider when it is moved
    def xChangeValue(self, value):
        try:
            # modifier = how many ticks are moved at a time
            modifier = value - self.old_xlim
            self.old_xlim = value
            old_min, old_max = self.sc.axes.get_xlim()
            # move the window accordingly
            self.sc.axes.set_xlim([old_min+(modifier),old_max+(modifier)])
            self.sc.draw()
        except:
            return
    
    # called by the y slider when it is moved
    def yChangeValue(self, value):
        try:
            # modifier = how many ticks are moved at a time        
            modifier = value - self.old_ylim
            self.old_ylim = value
            old_min, old_max = self.sc.axes.get_ylim()
            # move the window accordingly        
            self.sc.axes.set_ylim([old_min+(-1*modifier),old_max+(-1*modifier)])
            self.sc.draw()        
            return
        except:
            return



    # called by the self entered cmap option, sets the cmap to whatever is entered
    def setCustom(self):
        try:
            self.cmap, ok = QtGui.QInputDialog.getText(self, 'Set Cmap', 'Cmap')
            self.setCmap(self.cmap)
        except:
            return
        
    # called by menu options and setCustom, sets cmap and redraws the plot 
    def setCmap(self, cmap):
        try:
            self.cmap = cmap         
            self.sc.compute_figure(file_name = self.path, cmap = self.cmap)
            self.sc.axes.set_xlim(int(self.window_dim[0]), int(self.window_dim[1]))
            self.sc.axes.set_ylim(int(self.window_dim[3]), int(self.window_dim[2]))
            self.sc.draw()
        except:
            return


    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()
        
    # opens file, shows entire plot, sets sliders to not being able to move
    def openFile(self):
        try:
            self.path = QtGui.QFileDialog.getOpenFileName()
            
            self.x_sld.setMaximum(0)        
            self.y_sld.setMaximum(0)
            self.x_sld.setValue(0)
            self.y_sld.setValue(0) 
            
            self.data_dim = self.sc.compute_figure(file_name = self.path, cmap = self.cmap)
            self.x_sld_max = self.data_dim[0]
            self.y_sld_max = self.data_dim[1]
        except:
            return

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