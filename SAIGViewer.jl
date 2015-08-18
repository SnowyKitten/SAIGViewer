using PyCall
@pyimport matplotlib.backends.backend_qt4agg as qt4agg
@pyimport PyQt4 as PyQt4
@pyimport matplotlib.figure as mplf
using Seismic

progname = "SAIGViewer V0.1"

    function ApplicationWindow(w)

        # resets to the default display
        function resetButton(a=false)
            # set sliders to have no values again
            x_sld[:setMaximum](0)        
            y_sld[:setMaximum](0)
            x_sld[:setValue](0)
            y_sld[:setValue](0)
        
            ax[:set_xlim](0, x_sld_max-1)
            ax[:set_ylim](y_sld_max-1,0)
            canvas[:draw]()   
        end

        # called by the Zoom button, creates a window that takes comma separated coordinates to zoom to
        function zoomDialog(a=false)
            tmp = PyQt4.QtGui[:QInputDialog]()
            text, ok = tmp[:getText](w,"Zoom", "Zoom to [Xmin, Xmax, Ymin, Ymax]")
            if ok
                text = string(text)
                # due to lack of auto string conversion, we have to remove QString elements ourselves to get desired text
                text = text[33:end-2]
                text = strip(text)
                window_dim = split(text,',')
            
                # change the slider bars so that you can move the slider, but not past the edges
                x_sld[:setMaximum](data_dim[2] - (int(window_dim[2]) - int(window_dim[1])) - 1)        
                y_sld[:setMaximum](data_dim[1] - (int(window_dim[4]) - int(window_dim[3])) - 1)               
                
                # set slider bars to approximately the correct location given a zoom            
                y_sld[:setValue](y_sld_max - int(window_dim[4]))
                x_sld[:setValue](int(window_dim[1]))
            
                ax[:set_xlim](int(window_dim[1]), int(window_dim[2]))
                ax[:set_ylim](int(window_dim[4]), int(window_dim[3]))
                canvas[:draw]()
            end
        end

        # called by changes in value of the x slider, moves the picture appropriately
        function xChangeValue(value,a=false)
            # modifier = how many ticks are moved at a time
            modifier = (value - old_xlim)
            old_xlim = value
            old_min, old_max = ax[:get_xlim]()
            # move the window accordingly
            ax[:set_xlim]([old_min+(modifier),old_max+(modifier)])
            canvas[:draw]()        
        end

        # called by changes in value of the y slider, moves the picture appropriately
        function yChangeValue(value,a=false)
            # modifier = how many ticks are moved at a time
            modifier = (value - old_ylim)
            old_ylim = value
            old_min, old_max = ax[:get_ylim]()
             # move the window accordingly
            ax[:set_ylim]([old_min+(-1*modifier),old_max+(-1*modifier)])
            canvas[:draw]()        
        end

        function openFile()
            path = PyQt4.QtGui[:QFileDialog]()[:getOpenFileName]()
            # due to lack of auto string conversion, we have to remove QString elements ourselves to get desired text
            path = string(path)
            # removes front 33 Qstring added characters, and remove 8 off the end, 2 random chars, and 6 of .seisd to comform with SeisRead
            path = path[33:end-8]

            x_sld[:setMaximum](0)        
            y_sld[:setMaximum](0)
            x_sld[:setValue](0)
            y_sld[:setValue](0) 
            
            data, header, status = SeisRead(path)
            SeisPlot(data, ["canvas" => ax])
            canvas[:draw]()
            # data_dim[1] = size of y
            # data_dim[2] = size of x
            data_dim = size(data)
            x_sld_max = data_dim[2]
            y_sld_max = data_dim[1]

            window_dim = 0, x_sld_max, 0, y_sld_max

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
            w[:close]()
        end

        # naturally gets called when window is closed for whatever reason
        function closeEvent(w, ce):
            fileQuit()
        end

        function colourPlot()
            SeisPlot(data, ["canvas" => ax, "cmap" => cmap])
            resetButton()
        end

        function wigglePlot()
            ax[:clear]()
            SeisPlot(data, ["canvas" => ax, "style" => "wiggles"])
            resetButton()
        end

        # called by the self entered cmap option, sets the cmap to whatever is entered
        function setCustom()
            tmp = PyQt4.QtGui[:QInputDialog]()
            cmap, ok = tmp[:getText](w, "Set Cmap", "Cmap")
            cmap = string(cmap)
            cmap = cmap[33:end-2]
            setCmap(cmap)
        end
        
        # called by menu options and setCustom, sets cmap and redraws the plot 
        function setCmap(cmap)
            try
                SeisPlot(data, ["canvas" => ax, "cmap" => cmap])
                ax[:set_xlim](int(window_dim[1]), int(window_dim[2])-1)
                ax[:set_ylim](int(window_dim[4])-1, int(window_dim[3]))
                canvas[:draw]()
            catch e
                return
            end
        end

        function setBlues()
            setCmap("Blues")
        end

        function setBuGn()
            setCmap("BuGn")
        end

        function setBuPu()
            setCmap("BuPu")
        end

        function setGnBu()
            setCmap("GnBu")
        end

        function setGreens()
            setCmap("Greens")
        end

        function setGreys()
            setCmap("Greys")
        end

        function setOranges()
            setCmap("Oranges")
        end

        function setOrRd()
            setCmap("OrRd")
        end

        function setPuBu()
            setCmap("PuBu")
        end

        function setPuBuGn()
            setCmap("PuBuGn")
        end

        function setPuRd()
            setCmap("PuRd")
        end

        function setPurples()
            setCmap("Purples")
        end

        function setRdPu()
            setCmap("RdPu")
        end

        function setReds()
            setCmap("Reds")
        end

        function setYlGnBu()
            setCmap("YlGnBu")
        end

        function setYlOrBr()
            setCmap("YlOrBr")
        end

        function setYlOrRd()
            setCmap("OrRd")
        end

        function setafmhot()
            setCmap("afmhot")
        end

        function setautumn()
            setCmap("autumn")
        end

        function setbone()
            setCmap("bone")
        end

        function setcool()
            setCmap("cool")
        end

        function setcopper()
            setCmap("copper")
        end

        function setgist_heat()
            setCmap("gist_heat")
        end

        function setgray()
            setCmap("gray")
        end

        function sethot()
            setCmap("hot")
        end

        function setpink()
            setCmap("pink")
        end

        function setspring()
            setCmap("spring")
        end

        function setsummer()
            setCmap("summer")
        end

        function setwinter()
            setCmap("winter")
        end  

        function setBrBG()
            setCmap("BrBG")
        end

        function setbwr()
            setCmap("bwr")
        end

        function setcoolwarm()
            setCmap("coolwarm")
        end

        function setPiYG()
            setCmap("PiYG")
        end

        function setPRGn()
            setCmap("PRGn")
        end

        function setPuOr()
            setCmap("PuOr")
        end

        function setRdBu()
            setCmap("RdBu")
        end

        function setRdGy()
            setCmap("RdGy")
        end

        function setRdYlBu()
            setCmap("RdYlBu")
        end

        function setRdYlGn()
            setCmap("RdYlGn")
        end

        function setSpectral()
            setCmap("Spectral")
        end

        function setseismic()
            setCmap("seismic")
        end

        function setAccent()
            setCmap("Accent")
        end

        function setDark2()
            setCmap("Dark2")
        end

        function setPaired()
            setCmap("Paired")
        end

        function setPastel1()
            setCmap("Pastel1")
        end

        function setPastel2()
            setCmap("Pastel2")
        end

        function setSet1()
            setCmap("Set1")
        end

        function setSet2()
            setCmap("Set2")
        end

        function setSet3()
            setCmap("Set3")
        end

        function setgist_earth()
            setCmap("gist_earth")
        end

        function setterrain()
            setCmap("terrain")
        end

        function setocean()
            setCmap("ocean")
        end

        function setgist_stern()
            setCmap("gist_stern")
        end

        function setbrg()
            setCmap("brg")
        end

        function setCMRmap()
            setCmap("CMRmap")
        end

        function setcubehelix()
            setCmap("cubehelix")
        end

        function setgnuplot()
            setCmap("gnuplot")
        end

        function setgnuplot2()
            setCmap("gnuplot2")
        end

        function setgist_ncar()
            setCmap("gist_ncar")
        end

        function setnipy_spectral()
            setCmap("nipy_spectral")
        end

        function setjet()
            setCmap("jet")
        end

        function setrainbow()
            setCmap("rainbow")
        end

        function setgist_rainbow()
            setCmap("gist_rainbow")
        end

        function sethsv()
            setCmap("hsv")
        end          

        function setflag()
            setCmap("flag")
        end

        function setprism()
            setCmap("prism")
        end


        data = []
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
        zbtn[:clicked][:connect](zoomDialog)

        rbtn = PyQt4.QtGui[:QPushButton]("Reset")
        rbtn[:clicked][:connect](resetButton)


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


        # at startup, just have an empty plot to show
        ax[:plot]()

        l[:addWidget](y_sld, 0, 0)
        l[:addWidget](canvas, 0, 1)
        l[:addWidget](x_sld, 1, 1)
        l[:addWidget](zbtn, 2, 2)
        l[:addWidget](rbtn, 1, 2)

        # add all the menu options
        file_menu = PyQt4.QtGui[:QMenu]("&File", w)
        # again, values must be used because passing parameters by name betweens enums and 3 languages is hard
        # 0x04000000 == Qt.ControlModifier 0x4f == Qt.Key_O
        file_menu[:addAction]("&Open File...", openFile, int(0x04000000) + int(0x4f))
        # 0x41 == Qt.Key_A
        file_menu[:addAction]("&About", about, int(0x04000000) + int(0x41))     
        # 0x51 == Qt.Key_Q
        file_menu[:addAction]("&Quit", fileQuit, int(0x04000000) + int(0x51))
        
        style_menu = PyQt4.QtGui[:QMenu]("&Plot Style", w)
        style_menu[:addAction]("&Colour Plot", colourPlot)
        style_menu[:addAction]("&Wiggle Plot", wigglePlot)

        colour_menu = PyQt4.QtGui[:QMenu]("&Colour Map", w)    
        seqcmap_menu = PyQt4.QtGui[:QMenu]("&Sequential", w)
        seqcmap2_menu = PyQt4.QtGui[:QMenu]("&Sequential (2)", w)
        divcmap_menu = PyQt4.QtGui[:QMenu]("&Diverging", w)
        qualcmap_menu = PyQt4.QtGui[:QMenu]("&Qualitative", w)
        misccmap_menu = PyQt4.QtGui[:QMenu]("&Miscellaneous", w)
        
        colour_menu[:addMenu](seqcmap_menu)
        colour_menu[:addMenu](seqcmap2_menu)
        colour_menu[:addMenu](divcmap_menu)
        colour_menu[:addMenu](qualcmap_menu)
        colour_menu[:addMenu](misccmap_menu)
        
        seqcmap_menu[:addAction]("&Blues", setBlues)
        seqcmap_menu[:addAction]("&BuGn", setBuGn)
        seqcmap_menu[:addAction]("&BuPu", setBuPu)
        seqcmap_menu[:addAction]("&GnBu", setGnBu)
        seqcmap_menu[:addAction]("&Greens", setGreens)                        
        seqcmap_menu[:addAction]("&Greys", setGreys)        
        seqcmap_menu[:addAction]("&Oranges", setOranges)
        seqcmap_menu[:addAction]("&OrRd", setOrRd)        
        seqcmap_menu[:addAction]("&PuBu", setPuBu)
        seqcmap_menu[:addAction]("&PuBuGn", setPuBuGn)
        seqcmap_menu[:addAction]("&PuRd", setPuRd)
        seqcmap_menu[:addAction]("&Purples", setPurples)
        seqcmap_menu[:addAction]("&RdPu", setRdPu)        
        seqcmap_menu[:addAction]("&Reds", setReds)        
        seqcmap_menu[:addAction]("&YlGnBu", setYlGnBu)
        seqcmap_menu[:addAction]("&YlOrBr", setYlOrBr)        
        seqcmap_menu[:addAction]("&YlOrRd", setYlOrRd)

        seqcmap2_menu[:addAction]("&afmhot", setafmhot)
        seqcmap2_menu[:addAction]("&autumn", setautumn)
        seqcmap2_menu[:addAction]("&bone", setbone)
        seqcmap2_menu[:addAction]("&cool", setcool)
        seqcmap2_menu[:addAction]("&copper", setcopper)
        seqcmap2_menu[:addAction]("&gist_heat", setgist_heat)
        seqcmap2_menu[:addAction]("&gray", setgray)
        seqcmap2_menu[:addAction]("&hot", sethot)
        seqcmap2_menu[:addAction]("&pink", setpink)
        seqcmap2_menu[:addAction]("&spring", setspring)
        seqcmap2_menu[:addAction]("&summer", setsummer)
        seqcmap2_menu[:addAction]("&winter", setwinter)
        
        divcmap_menu[:addAction]("&BrBG", setBrBG)
        divcmap_menu[:addAction]("&bwr", setbwr)
        divcmap_menu[:addAction]("&coolwarm", setcoolwarm)
        divcmap_menu[:addAction]("&PiYG", setPiYG)
        divcmap_menu[:addAction]("&PRGn", setPRGn)
        divcmap_menu[:addAction]("&PuOr", setPuOr)
        divcmap_menu[:addAction]("&RdBu", setRdBu)
        divcmap_menu[:addAction]("&RdGy", setRdGy)
        divcmap_menu[:addAction]("&RdYlBu", setRdYlBu)
        divcmap_menu[:addAction]("&RdYlGn", setRdYlGn)
        divcmap_menu[:addAction]("&Spectral", setSpectral)
        divcmap_menu[:addAction]("&seismic", setseismic)

        qualcmap_menu[:addAction]("&Accent", setAccent)
        qualcmap_menu[:addAction]("&Dark2", setDark2)
        qualcmap_menu[:addAction]("&Paired", setPaired)
        qualcmap_menu[:addAction]("&Pastel1", setPastel1)
        qualcmap_menu[:addAction]("&Pastel2", setPastel2)
        qualcmap_menu[:addAction]("&Set1", setSet1)
        qualcmap_menu[:addAction]("&Set2", setSet2)
        qualcmap_menu[:addAction]("&Set3", setSet3)
        
        misccmap_menu[:addAction]("&gist_earth", setgist_earth)
        misccmap_menu[:addAction]("&terrain", setterrain)
        misccmap_menu[:addAction]("&ocean", setocean)
        misccmap_menu[:addAction]("&gist_stern", setgist_stern)
        misccmap_menu[:addAction]("&brg", setbrg)
        misccmap_menu[:addAction]("&CMRmap", setCMRmap)
        misccmap_menu[:addAction]("&cubehelix", setcubehelix)
        misccmap_menu[:addAction]("&gnuplot", setgnuplot)
        misccmap_menu[:addAction]("&gnuplot2", setgnuplot2)
        misccmap_menu[:addAction]("&gist_ncar", setgist_ncar)
        misccmap_menu[:addAction]("&nipy_spectral", setnipy_spectral)
        misccmap_menu[:addAction]("&jet", setjet)
        misccmap_menu[:addAction]("&rainbow", setrainbow)
        misccmap_menu[:addAction]("&gist_rainbow", setgist_rainbow)
        misccmap_menu[:addAction]("&hsv", sethsv)
        misccmap_menu[:addAction]("&flag", setflag)
        misccmap_menu[:addAction]("&prism", setprism)   

        colour_menu[:addAction]("&Enter a cmap" , setCustom)

        w[:menuBar]()[:addMenu](file_menu)
        w[:menuBar]()[:addMenu](colour_menu)
        w[:menuBar]()[:addMenu](style_menu)

        main_widget[:setFocus]()
        w[:setCentralWidget](main_widget)

        return w
    end

qApp = PyQt4.QtGui[:QApplication](ARGS)
window = PyQt4.QtGui[:QMainWindow]()
window[:setWindowTitle]("SAIGViewer")

aw = ApplicationWindow(window)
aw[:setWindowTitle](progname)
aw[:show]()

qApp[:exec_]()

