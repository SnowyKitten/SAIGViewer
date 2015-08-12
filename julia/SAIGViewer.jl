using PyCall
@pyimport matplotlib.backends.backend_qt4agg as qt4agg
@pyimport PyQt4 as PyQt4
@pyimport matplotlib.figure as mplf
using Seismic


progname = "SAIGViewer V0.1"
file_name = "small_stack"

    function ApplicationWindow(w)

        w = PyQt4.QtGui[:QMainWindow]()        # constructors
        w[:setWindowTitle](progname) # w.setWindowTitle() is w[:setWindowTitle] in PyCall
          
        main_widget = PyQt4.QtGui[:QWidget](w)

        l = PyQt4.QtGui[:QGridLayout](main_widget)


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
      
 
        d, h, status = SeisRead(file_name)        

        SeisPlot(d,["canvas" => ax, "style" => "wiggles"])


        l[:addWidget](canvas,0,1)

        main_widget[:setFocus]()
        w[:setCentralWidget](main_widget)


        return w
    end


qApp = PyQt4.QtGui[:QApplication](ARGS)
window = PyQt4.QtGui[:QMainWindow]()
#window[:setAttribute](PyQt4.QtCore.Qt.Wa_DeleteOnClose)
window[:setWindowTitle]("SAIGViewer")

aw = ApplicationWindow(window)
aw[:setWindowTitle](progname)
aw[:show]()



if !isinteractive()
    wait(Condition())
end































#=
btn = Qt.QPushButton("Click me", w)
lyt[:addWidget](btn)
qconnect(btn, :clicked) do  # qconnect convenience to connect to a signal
    msg = Qt.QMessageBox(btn)
    msg[:setWindowTitle]("A message for you...")
    msg[:setText]("Hello world!")
    msg[:setInformativeText]("Thanks for clicking.")
    msg[:setIcon](Qt.QMessageBox()[:Information])   # how to pick out Qt::QMessageBox::Information 
enumeration
  convert(Function, msg[:exec])()       # Sometimes, one must must convert to a function (or call qexec(msg))
end
=#
