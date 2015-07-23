@doc """
       Make 2D plots. Blah Blah.
       """ ->
    function SeisPlot(in,param)

    style = get(param,"style","color") # color or wiggles
    wiggle_fill_color = get(param,"wiggle_fill_color","k") # fill color for wiggles
    wiggle_line_color = get(param,"wiggle_line_color","k") # line color for wiggles
    wiggle_trace_increment = get(param,"wiggle_trace_increment",1) # can skip traces for wiggles
    xcur = get(param,"xcur",1.2) # wiggle excursion if wiggles selected
	fignum = get(param,"fignum",1)
	cmap = get(param,"cmap","RdGy")
	aspect = get(param,"aspect",2)
	vmin = get(param,"vmin",-1)
	vmax = get(param,"vmax",1)
	title  = get(param,"title"," ")
	xlabel = get(param,"xlabel"," ")
	xunits = get(param,"xunits"," ")
	ylabel = get(param,"ylabel"," ")
	yunits = get(param,"yunits"," ")
	ox = get(param,"ox",0)
	dx = get(param,"dx",1)
	oy = get(param,"oy",0)
	dy = get(param,"dy",1)
	dpi = get(param,"dpi",100)
	wbox = get(param,"wbox",8)
	hbox = get(param,"hbox",8)
	name = get(param,"name","NULL")
	interpolation = get(param,"interpolation","none")
	
	fig = plt.figure(num=fignum, figsize=(wbox, hbox), dpi=dpi, facecolor="w", edgecolor="k")
	if (style != "wiggles")
		plt.imshow(in,cmap=cmap,vmin=vmin,vmax=vmax,extent=[ox,ox + (size(in,2)-1)*dx,oy + (size(in,1)-1)*dy,oy],aspect=aspect)
	end
    if (style != "color")
		y = oy+dy*[0:1:size(in,1)-1]
		x = ox+dx*[0:1:size(in,2)-1]
		delta = wiggle_trace_increment*dx
		hmin = minimum(x)
		hmax = maximum(x)
		dmax = maximum(in[:])
		alpha = xcur*delta/dmax
		for k = 1:wiggle_trace_increment:size(in,2)
 			s = in[:,k]
 			s[1]=0
 			s[size(in,1)]=0
 			sp = (s+abs(s))/2. 
 			plt.plot( s*alpha + x[k],y,wiggle_line_color)
 			if (style != "overlay") 
 				plt.fill(sp*alpha + x[k],y,wiggle_fill_color)
 			end
		end
		plt.axis([ox,ox + (size(in,2)-1)*dx,oy + (size(in,1)-1)*dy,oy])
	end
	plt.title(title)
	plt.xlabel(join([xlabel " " xunits]))
	plt.ylabel(join([ylabel " " yunits]))
		
	if (name == "NULL")
	  plt.show()
	else  
      plt.savefig(name,dpi=dpi)
      plt.close()
    end
	
end
