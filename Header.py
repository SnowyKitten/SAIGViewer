class Header: 
    header_count = dict()
    header_count["tracenum"] = 0
    header_count["o1"]    = 1
    header_count["n1"]    = 2
    header_count["d1"]    = 3
    header_count["sx"]    = 4
    header_count["sy"]    = 5
    header_count["gx"]    = 6
    header_count["gy"]    = 7
    header_count["mx"]    = 8
    header_count["my"]    = 9
    header_count["hx"]    = 10
    header_count["hy"]    = 11
    header_count["h"]     = 12
    header_count["az"]    = 13
    header_count["ang"]   = 14
    header_count["isx"]   = 15
    header_count["isy"]   = 16
    header_count["igx"]   = 17
    header_count["igy"]   = 18
    header_count["imx"]   = 19
    header_count["imy"]   = 20
    header_count["ihx"]   = 21
    header_count["ihy"]   = 22
    header_count["ih"]    = 23
    header_count["iaz"]   = 24
    header_count["iang"]  = 25
    header_count["selev"] = 26
    header_count["gelev"] = 27
    header_count["sstat"] = 28
    header_count["gstat"] = 29
    header_count["trid"]  = 30        
    
    def __init__(self):
	self.tracenum = int(0)
        self.o1  = float(0)
        self.n1  = int(0)
        self.d1  = float(0)
        self.sx  = float(0)
        self.sy  = float(0)
        self.gx  = float(0)
        self.gy  = float(0)
        self.mx  = float(0)
        self.my  = float(0)
        self.hx  = float(0)
        self.hy  = float(0)
        self.h   = float(0)
	self.az  = float(0)
        self.ang = float(0)
        self.isx = int(0)
        self.isy = int(0)
        self.igx = int(0)
        self.igy = int(0)
        self.imx = int(0)
        self.imy = int(0)
        self.ihx = int(0)
        self.ihy = int(0)
        self.ih  = int(0)
        self.iaz = int(0)
        self.iang= int(0)
        self.selev = float(0)
        self.gelev = float(0)
        self.sstat = float(0)
        self.gstat = float(0)
        self.trid  = float(0)



    def set_header(self, header_list):
        self.tracenum = header_list[0]
        self.o1    = header_list[1]
        self.n1    = header_list[2]
        self.d1    = header_list[3]
        self.sx    = header_list[4]
        self.sy    = header_list[5]
        self.gx    = header_list[6]
        self.gy    = header_list[7]
        self.mx    = header_list[8]
        self.my    = header_list[9]
        self.hx    = header_list[10]
        self.hy    = header_list[11]
        self.h     = header_list[12]
        self.az    = header_list[13]
        self.ang   = header_list[14]
        self.isx   = header_list[15]
        self.isy   = header_list[16]
        self.igx   = header_list[17]
        self.igy   = header_list[18]
        self.imx   = header_list[19]
        self.imy   = header_list[20]
        self.ihx   = header_list[21]
        self.ihy   = header_list[22]
        self.ih    = header_list[23]
        self.iaz   = header_list[24]
        self.iang   = header_list[25]
        self.selev = header_list[26]
        self.gelev = header_list[27]
        self.sstat = header_list[28]
        self.gstat = header_list[29]
        self.trid  = header_list[30]


    def get_header(self):
        header_list = []
	header_list.append(self.tracenum)
        header_list.append(self.o1)
        header_list.append(self.n1)
	header_list.append(self.d1)
	header_list.append(self.sx)
	header_list.append(self.sy)
	header_list.append(self.gx)
	header_list.append(self.gy)
	header_list.append(self.mx)
	header_list.append(self.my)
	header_list.append(self.hx)
	header_list.append(self.hy)
	header_list.append(self.h)
	header_list.append(self.az)
	header_list.append(self.ang)
	header_list.append(self.isx)
	header_list.append(self.isy)
	header_list.append(self.igx)
	header_list.append(self.igy)
	header_list.append(self.imx)
	header_list.append(self.imy)
	header_list.append(self.ihx)
	header_list.append(self.ihy)
	header_list.append(self.ih)
	header_list.append(self.iaz)
	header_list.append(self.iang)
	header_list.append(self.selev)
	header_list.append(self.gelev)
	header_list.append(self.sstat)
	header_list.append(self.gstat)
	header_list.append(self.trid)
