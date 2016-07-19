'''
Created on Jun 30, 2016

@author: nivek
'''
from MemoryDriver import MemoryDriver
from SetOfVerticesAndEdges import SetOfVerticesAndEdges
from PyQt4.Qt import QVariant
from timeit import default_timer as timer

from qgis.utils import iface
#from CleanSOVAE import CleanSOVAE

# import sys

# from qgis.core import QgsApplication
# QgsApplication.setPrefixPath("/home/tleduc/prj/t4qg/graph/src", True)

# sys.path.append(r'/home/nivek/Programs/eclipse/Workspace/graph/src')
'''
print "toto"
for feature in qgis.utils.iface.activeLayer().getFeatures():
    mytype = feature.geometry().type(); 
    if QGis.Line == mytype:
        print "ok ok ok ______"
    else:
        print "pas ok"

    print "mytype = %s" % mytype
    
    if 'l' == mytype:
        print "ok ok ok ok"
    else:
        print "pas ok ok"
    break;

exit;

start = timer()
'''
start = timer()
layer = iface.activeLayer()
print("Layername: %s") % layer.name()
#distance= int(raw_input('what distance?'))
#print distance
 
#~ ======================================================================
if not layer is None:
    sovae = CleanSOVAE()
    sovae.add(layer.getFeatures())
    
    cnt = 0
    for feature in layer.getFeatures():
        cnt += 1
        
    print cnt
    rs = sovae.getUniqueRoadsSections()
#    print "RS",rs
    rsi = sovae.get_Intersections(10)
#    rsd = sovae.getDividedRoadsSections()
    rs = sovae.getUniqueRoadsSections()
    #rsa = sovae.devideTroncon(rs)
#    print "rsi:",rsi
#    print("Nb of roads sections nodes: %d") % len(rsi)
 
    #~ ====================================================================== CREATE LAYER
    fields = [  ]  #{"name":"distance nb i", "type":QVariant.String},  { "name":"angles", "type":QVariant.String }
    for intersectionD in rsi:
        #GET MAX LEN OF INTD.VALUES
        for distance in intersectionD.iterkeys():
            if distance != 'the_geom':
                fields.append({"name":distance, "type":QVariant.String})
#        print fields
    memDriver = MemoryDriver("Point", "angles", fields) #"distance",
    memDriver.addFeatures(rsi)
    
    #~ ====================================================================== CREATE PLOT

    

stop = timer()
print "Elapsed time: %f s" % (stop - start)
