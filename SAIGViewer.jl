using PyCall
@pyimport matplotlib.backends.backend_qt4agg as qt4agg
@pyimport PyQt4 as PyQt4
@pyimport matplotlib.figure as mplf
#unshift!(PyVector(pyimport("sys")["path"]), "")
#@pyimport SAIGFunc as saigf

using Seismic



progname = "SAIGViewer V0.1"
file_name = "binary_data/data_with_noise"

    function ApplicationWindow(w)
        path = ""
        old_xlim = 0
        old_ylim = 0
        x_sld_max = 100
        y_sld_max = 100
        data_dim = 0,0
        window_dim = 0,0
        style = "color" 
        wiggle_fill_color = "k"
        wiggle_line_color = "k"
        wiggle_trace_increment = 1
        xcur = 1.2
        fignum = 1
        cmap = "RdGy"
        vmin = -1
        vmax = 1
        title = " "
        xlabel = " "
        xunits = " "
        ylabel = " "
        yunits = " "
        ox = 0
        dx = 1
        oy = 0
        dy = 1
        dpi = 100
        wbox = 8
        hbox = 8
        name = None
        interpolation = nothing 



        w = PyQt4.QtGui[:QMainWindow]()        # constructors
        w[:setWindowTitle](progname) # w.setWindowTitle() is w[:setWindowTitle] in PyCall
          
        main_widget = PyQt4.QtGui[:QWidget](w)

        l = PyQt4.QtGui[:QGridLayout](main_widget)

        app_icon = PyQt4.QtGui[:QIcon]()
        app_icon[:addFile]("Icons/SAIG16x16.png", PyQt4.QtCore[:QSize](16,16))
        app_icon[:addFile]("Icons/SAIG24x24.png", PyQt4.QtCore[:QSize](24,24))
        app_icon[:addFile]("Icons/SAIG32x32.png", PyQt4.QtCore[:QSize](32,32))
        app_icon[:addFile]("Icons/SAIG48x48.png", PyQt4.QtCore[:QSize](48,48))
        app_icon[:addFile]("Icons/SAIG256x256.png", PyQt4.QtCore[:QSize](256,256))        
        w[:setWindowIcon](app_icon)

        width = 4
        height = 4
        dpi = 100
        fig = mplf.Figure((width,height), dpi)
        szp = PyQt4.QtGui[:QSizePolicy]()
        canvas = qt4agg.FigureCanvasQTAgg(fig)
        canvas[:setSizePolicy](szp[:Expanding],
                               szp[:Expanding])
        canvas[:updateGeometry]()
        ax = fig[:add_subplot](1,1,1)
        ax[:hold](false)
      

        zbtn = PyQt4.QtGui[:QPushButton]("Zoom")
        function zoomDialog(a=false)
            tmp = PyQt4.QtGui[:QInputDialog]()
            text, ok = tmp[:getText](w,"Zoom", "Zoom to [Xmin, Xmax, Ymin, Ymax]")
            if ok
                text = string(text)
                text = text[33:end-2]
                text = strip(text)
                window_dim = split(text,',')
            #=
                # change the slider bars so that you can move the slider, but not past the edges
                self.x_sld.setMaximum(self.data_dim[0] - (int(self.window_dim[1]) - int(self.window_dim[0])))        
                self.y_sld.setMaximum(self.data_dim[1] - (int(self.window_dim[3]) - int(self.window_dim[2])))               
                
                # set slider bars to approximately the correct location given a zoom            
                self.y_sld.setValue(self.y_sld_max - int(self.window_dim[3]))
                self.x_sld.setValue(int(self.window_dim[0]))
            =#
                ax[:set_xlim](int(window_dim[1]), int(window_dim[2]))
                ax[:set_ylim](int(window_dim[4]), int(window_dim[3]))
                canvas[:draw]()

            end
        end
        zbtn[:clicked][:connect](zoomDialog)
  

        function xChangeValue(value,a=false)
            # modifier = how many ticks are moved at a time
            modifier = (value - old_xlim)
            old_xlim = value
            old_min, old_max = ax[:get_xlim]()
            # move the window accordingly
            ax[:set_xlim]([old_min+(modifier),old_max+(modifier)])
            canvas[:draw]()        
        end
        # create the x-axis pan slider
        x_sld = PyQt4.QtGui[:QSlider]()
        # 0x1 == Horizontal, QtCore.Qt.Horizontal
        x_sld[:setOrientation](int(0x1))
        # 0 == NoFocus, QtCore.Qt.NoFocus
        x_sld[:setFocusPolicy](int(0))
        x_sld[:setTickPosition](1)
        x_sld[:setMinimum](0)
        x_sld[:setMaximum](x_sld_max)
        x_sld[:setTickInterval](4)
        x_sld[:setRange](0,x_sld_max)
        x_sld[:setValue](x_sld_max//2)
        x_sld[:valueChanged][:connect](xChangeValue)   



        
        function yChangeValue(value,a=false)
            # modifier = how many ticks are moved at a time
            modifier = (value - old_ylim)
            old_ylim = value
            old_min, old_max = ax[:get_ylim]()
             # move the window accordingly
            ax[:set_ylim]([old_min+(modifier),old_max+(modifier)])
            canvas[:draw]()        
        end       
        # create the x-axis pan slider
        y_sld = PyQt4.QtGui[:QSlider]()
        # 0x2 == Vertical, QtCore.Qt.Vertical
        y_sld[:setOrientation](int(0x2))
        # 0 == NoFocus, QtCore.Qt.NoFocus
        y_sld[:setFocusPolicy](int(0))
        y_sld[:setTickPosition](2)
        y_sld[:setMinimum](0)
        y_sld[:setMaximum](y_sld_max)
        y_sld[:setTickInterval](4)
        y_sld[:setRange](0,y_sld_max)
        y_sld[:setValue](y_sld_max//2)
        y_sld[:valueChanged][:connect](yChangeValue) 





        d, h, status = SeisRead(file_name)        

        SeisPlot(d,["canvas" => ax, "style" => "wiggles"])

        l[:addWidget](y_sld, 0, 0)
        l[:addWidget](canvas, 0, 1)
        l[:addWidget](x_sld, 1, 1)
        l[:addWidget](zbtn, 2, 2)
        #l[:addWidget](rbtn, 1, 2)



        function openFile()
            return
        end
        function about()
            tmp = PyQt4.QtGui[:QMessageBox]()

            tmp[:about](w, "About",
            """
            Simple Plot Viewer built for SAIG (Signal Analysis and Imaging Group) at the University of Alberta
            """
            )
        end
        function fileQuit()
            return
        end

        # add all the menu options
        file_menu = PyQt4.QtGui[:QMenu]("&File", w)
        # again, values must be used because passing parameters by name betweens enums and 3 languages is hard
        # 0x04000000 == Qt.ControlModifier 0x4f == Qt.Key_O
        file_menu[:addAction]("&Open File...", openFile, int(0x04000000) + int(0x4f))
        # 0x41 == Qt.Key_A
        file_menu[:addAction]("&About", about, int(0x04000000) + int(0x41))     
        # 0x51 == Qt.Key_Q
        file_menu[:addAction]("&Quit", fileQuit, int(0x04000000) + int(0x51))
        
        w[:menuBar]()[:addMenu](file_menu)






        main_widget[:setFocus]()
        w[:setCentralWidget](main_widget)





        return w
    end



#=
    def zoomDialog(self):
        
        text, ok = QtGui.QInputDialog.getText(self, 'Zoom', 'Zoom to [Xmin, Xmax, Ymin, Ymax]')
        if ok:
                text = str(text)
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
=#


qApp = PyQt4.QtGui[:QApplication](ARGS)
window = PyQt4.QtGui[:QMainWindow]()
window[:setWindowTitle]("SAIGViewer")



aw = ApplicationWindow(window)
aw[:setWindowTitle](progname)
aw[:show]()


if !isinteractive()
    wait(Condition())
end
