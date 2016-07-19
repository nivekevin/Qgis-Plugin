'''
Created on 30 mai 2016

@author: tleduc

OUVRIR LA CONSOLE PYTHON DE QGIS : CTRL + ALT + P
execfile('d:/tleduc/prj/t4qg/graph/src/STToRoadsSectionsNodes.py')
execfile('/home/tleduc/prj/t4qg/graph/src/STToRoadsSectionsNodes.py')
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
    rsn = sovae.getUniqueRoadsSectionsNodes()
    print("Nb of nodes: %d") % len(rsn)

    #~ ======================================================================
    fields = [ { "name":"nb_connections", "type":QVariant.Int } ]    
    memDriver = MemoryDriver("Point", "roads_sections_nodes", fields)
    memDriver.addFeatures(rsn)

stop = timer()
print "Elapsed time: %f s" % (stop -start)
