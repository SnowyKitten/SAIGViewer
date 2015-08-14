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
  


        d, h, status = SeisRead(file_name)        

        SeisPlot(d,["canvas" => ax, "style" => "wiggles"])

        #l[:addWidget](y_sld, 0, 0)
        l[:addWidget](canvas, 0, 1)
        #l[:addWidget](x_sld, 1, 1)
        l[:addWidget](zbtn, 2, 2)
        #l[:addWidget](rbtn, 1, 2)




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
