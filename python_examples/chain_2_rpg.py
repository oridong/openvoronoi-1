import openvoronoi as ovd
import ovdvtk
import time
import vtk
import datetime
import math
import random
import os
import sys
import pickle
import gzip
import ovdgenerators as gens
import rpg

if __name__ == "__main__":  
    #print ocl.revision()
    #w=2500
    #h=1500
    
    #w=1920
    #h=1080
    w=1024
    h=1024
    myscreen = ovdvtk.VTKScreen(width=w, height=h) 
    ovdvtk.drawOCLtext(myscreen, rev_text=ovd.revision() )
    
    w2if = vtk.vtkWindowToImageFilter()
    w2if.SetInput(myscreen.renWin)
    lwr = vtk.vtkPNGWriter()
    lwr.SetInput( w2if.GetOutput() )
    #w2if.Modified()
    #lwr.SetFileName("tux1.png")
    
    scale=1
    myscreen.render()
    random.seed(42)
    far = 1
    camPos = far
    zmult = 3
    # camPos/float(1000)
    myscreen.camera.SetPosition(0, -camPos/float(1000), zmult*camPos) 
    myscreen.camera.SetClippingRange(-(zmult+1)*camPos,(zmult+1)*camPos)
    myscreen.camera.SetFocalPoint(0.0, 0, 0)
    
    vd = ovd.VoronoiDiagram(far,120)
    print vd.version()
    
    # for vtk visualization
    vod = ovdvtk.VD(myscreen,vd,float(scale), textscale=0.01, vertexradius=0.003)
    vod.drawFarCircle()

    
    vod.textScale = 0.02
    vod.vertexRadius = 0.0031
    vod.drawVertices=1
    #vod.drawVertexIndex=0
    vod.drawGenerators=1
    
    vod.offsetEdges = 1
    vd.setEdgeOffset(0.05)
    
    
    linesegs = 1 # switch to turn on/off line-segments
    
    Npts = 4
    poly = rpg.rpg(Npts)
    pts=[]
    for p in poly:
        pts.append( ovd.Point( p[0], p[1] ) )
        
    times=[]
    id_list = []
    m=0
    t_before = time.time()
    for p in pts:
        id_list.append( vd.addVertexSite( p ) )
        print m," added vertex "
        m=m+1
    print "polygon is: "
    for idx in id_list:
        print idx," ",
    print "."
    
    t_after = time.time()
    times.append( t_after-t_before )
    
    print "all point sites inserted. ",
    vd.check()
    
    t_before = time.time()
    if linesegs==1:
        for n in range(len(id_list)):
            n_nxt = n+1
            if n==(len(id_list)-1):
                n_nxt=0
            vd.addLineSite( id_list[n], id_list[n_nxt])
        
    vd.check()
    
    
    t_after = time.time()
    line_time = t_after-t_before
    if line_time < 1e-3:
        line_time = 1
    times.append( line_time )
    
    #s = id_list[nsegs]
    #vd.debug_on()
    #vd.addLineSite( s[0], s[1], 10) 
    #seg = id_list[nsegs]
    #vd.addLineSite(seg[0],seg[1],10)
    # 1 identify start/endvert
    # 2 add line-segment edges/sites to graph
    # 3 identify seed-vertex
    # 4 create delete-tree
    # 5 create new vertices
    # 6 add startpoint pos separator
    # 7 add startoiubt neg separator
    # 8 add end-point pos separator
    # 9 add end-point neg separator
    # 10 add new edges
    # 11 delete delete-tree edges
    # 12 reset status
            
    vod.setVDText2(times)
    
    err = vd.getStat()
    #print err 
    print "got errorstats for ",len(err)," points"
    if len(err)>1:
        minerr = min(err)
        maxerr = max(err)
        print "min error= ",minerr
        print "max error= ",maxerr
    
    print "num vertices: ",vd.numVertices() 
    print "num SPLIT vertices: ",vd.numSplitVertices() 
        
    calctime = t_after-t_before
    
    vod.setAll()
        
    print "PYTHON All DONE."

    myscreen.render()   
    #w2if.Modified()
    #lwr.SetFileName("{0}.png".format(Nmax))
    #lwr.Write()
     
    myscreen.iren.Start()
