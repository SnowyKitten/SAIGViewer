from pylab import *

data_long_vector = fromfile("small_stack.seisd", dtype=float32)
print(len(data_long_vector))
data_matrix = data_long_vector.reshape((200, 20), order="FORTRAN")
print(data_matrix)
imshow(data_matrix,aspect='equal')
show()