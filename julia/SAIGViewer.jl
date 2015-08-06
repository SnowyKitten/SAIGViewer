using PyCall
@pyimport matplotlib.backends.backend_qt4agg as qt4agg
#using PySide
@pyimport PyQt4 as PyQt4
using PyPlot
using Seismic


progname = "SAIGViewer V0.1"
file_name = "data_with_noise.seisd"

    function ApplicationWindow(w)

        w = PyQt4.QtGui[:QMainWindow]()        # constructors
        w[:setWindowTitle](progname) # w.setWindowTitle() is w[:setWindowTitle] in PyCall
          
        main_widget = PyQt4.QtGui[:QWidget](w)

        l = PyQt4.QtGui[:QGridLayout](main_widget)
        w[:setLayout](l)

        width = 4
        height = 4
        dpi = 100

        fig = figure(0,(width,height), dpi)

        canvas = qt4agg.FigureCanvasQTAgg(fig)
        canvas[:setSizePolicy](canvas,
                              PyQt4.QtGui[:QSizePolicy]()[:Expanding](),
                              PyQt4.QtGui[:QSizePolicy]()[:Expanding]())
        canvas[:updateGeometry](canvas)

        ax = fig[:add_subplot](1,1,1)

        d = rand(100,100)

        SeisPlot(d,["canvas" => ax])

        l[:addWidget](canvas)

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
