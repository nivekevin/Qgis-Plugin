'''
Created on 31 mai 2016

@author: tleduc

OUVRIR LA CONSOLE PYTHON DE QGIS : CTRL + ALT + P
execfile('d:/tleduc/prj/t4qg/graph/src/STToRoadsSections.py')
execfile('/home/tleduc/prj/t4qg/graph/src/STToRoadsSections.py')
'''
import qgis.utils

from MemoryDriver import MemoryDriver
from SetOfVerticesAndEdges import SetOfVerticesAndEdges
from PyQt4.Qt import QVariant
from timeit import default_timer as timer

# from qgis.core import QgsApplication
# QgsApplication.setPrefixPath("/home/tleduc/prj/t4qg/graph/src", True)

start = timer()

layer = iface.activeLayer()
print("Layername: %s") % layer.name()

#~ ======================================================================
if not layer is None:
    sovae = SetOfVerticesAndEdges()
    sovae.add(layer.getFeatures())
    rs = sovae.getUniqueRoadsSections()
    print("Nb of roads sections: %d") % len(rs)

    #~ ======================================================================
    fields = [ { "name":"distance", "type":QVariant.Double } ]    
    memDriver = MemoryDriver("LineString", "roads_sections", fields)
    memDriver.addFeatures(rs)

stop = timer()
print "Elapsed time: %f s" % (stop -start)
