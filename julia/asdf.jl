using PyCall
@pyimport matplotlib.backends.backend_qt4agg as qt4agg
@pyimport PyQt4 as PyQt4
@pyimport matplotlib.figure as mplf
using Seismic
x_entries = Float64[]
y_entries = Float64[]

push!(x_entries, 1)
push!(y_entries, 2)

println(x_entries)
println(y_entries)
