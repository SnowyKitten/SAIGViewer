from pylab import *
import numpy as np
import struct

class DataReader():
    
    def __init__(self):
        return
    
    def read_header(self, file_name_h):
        header_matrix = []        
        with open(file_name_h, "rb") as f:
            byte = f.read(124)
            while byte:
                # create a list that holds all header attributes in order
                tmp = []
                
                # struct.unpack returns a tuple, even of one entry, so getting [0] of it returns the actual value
                tmp.append(struct.unpack('i', byte[0:4])[0])      # tracenum (int)
                tmp.append(struct.unpack('f', byte[4:8])[0])      # o1 (float)      
                tmp.append(struct.unpack('i', byte[8:12])[0])     # n1 (int)
                tmp.append(struct.unpack('f', byte[12:16])[0])    # d1 (float)
                tmp.append(struct.unpack('f', byte[16:20])[0])    # sx (float) 
                tmp.append(struct.unpack('f', byte[20:24])[0])    # sy (float)
                tmp.append(struct.unpack('f', byte[24:28])[0])    # gx (float)
                tmp.append(struct.unpack('f', byte[28:32])[0])    # gy (float)
                tmp.append(struct.unpack('f', byte[32:36])[0])    # mx (float
                tmp.append(struct.unpack('f', byte[36:40])[0])    # my (float)
                tmp.append(struct.unpack('f', byte[40:44])[0])    # hx (float)
                tmp.append(struct.unpack('f', byte[44:48])[0])    # hy (float)
                tmp.append(struct.unpack('f', byte[48:52])[0])    # h  (float)
                tmp.append(struct.unpack('f', byte[52:56])[0])    # az (float)
                tmp.append(struct.unpack('f', byte[56:60])[0])    # ang (float)
                tmp.append(struct.unpack('i', byte[60:64])[0])    # isx (int)
                tmp.append(struct.unpack('i', byte[64:68])[0])    # isy (int)
                tmp.append(struct.unpack('i', byte[68:72])[0])    # igx (int)
                tmp.append(struct.unpack('i', byte[72:76])[0])    # igy (int)
                tmp.append(struct.unpack('i', byte[76:80])[0])    # imx (int)
                tmp.append(struct.unpack('i', byte[80:84])[0])    # imy (int)
                tmp.append(struct.unpack('i', byte[84:88])[0])    # ihx (int)
                tmp.append(struct.unpack('i', byte[88:92])[0])    # ihy (int)
                tmp.append(struct.unpack('i', byte[92:96])[0])    # ih  (int)
                tmp.append(struct.unpack('i', byte[96:100])[0])   # iaz (int)
                tmp.append(struct.unpack('i', byte[100:104])[0])  # iang (int)
                tmp.append(struct.unpack('f', byte[104:108])[0])  # selev (float)
                tmp.append(struct.unpack('f', byte[108:112])[0])  # gelev (float)
                tmp.append(struct.unpack('f', byte[112:116])[0])  # sstat (float)
                tmp.append(struct.unpack('f', byte[116:120])[0])  # gstat (float)                 
                tmp.append(struct.unpack('i', byte[120:124])[0])  # trid (int)

                # add the header line into the header matrix, will be transposed later
                header_matrix.append(tmp)
                byte = f.read(124)
                
        f.close()    
        return np.array(header_matrix).transpose()
    
    
    def read_data(self, file_name):
        # gets the name of the header file
        file_name_h = file_name[:-1] + "h"
        header_matrix = self.read_header(file_name_h)
        
        f = open(file_name, 'rb')
        data_long_vector = fromfile(f, dtype=float32)
        
        # header_matrix[-1][0] is the tracenum of the last trace
        num_traces = header_matrix[0][-1]
        
        # n1 is taken directly from header, the length of the axis
        n1 = header_matrix[2][0]
        
        data_matrix = data_long_vector.reshape((n1, num_traces), order="FORTRAN")
        data_matrix = data_matrix.tolist()
        
        # for now just return the data matrix, header matrix is ignored
        return data_matrix
    
