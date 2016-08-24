'''
Created on 30 mai 2016

@author: tleduc
'''
from qgis.core import *
import numpy as np

class SetOfVerticesAndEdges():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.ciVertices = dict()
        self.icVertices = dict()
        self.edges = dict()
        
    def add(self, features):
        for feature in features:
            geom = feature.geometry()
            if QGis.Line == geom.type():
                self.__addPolyline(geom.asPolyline())
        #~ print "self.icVertices: %s" % self.icVertices
        #~ print "self.edges: %s" % self.edges

    def __addPolyline(self, coords):
        if (2 <= len(coords)):
            prev = self.__addAndGetANode(coords[0])
            for i in xrange(1, len(coords)):
                curr = self.__addAndGetANode(coords[i]);
                if self.edges.get(prev) is None:
                    self.edges[prev] = [ curr ]
                else:
                    self.edges[prev].append(curr)
                if self.edges.get(curr) is None:
                    self.edges[curr] = [ prev ]
                else:
                    self.edges[curr].append(prev)
                prev = curr;
            
    def __addAndGetANode(self, coord):
        str_coord = ("%f %f") % (coord[0], coord[1])
        if self.ciVertices.get(str_coord) is None:
            nodeIndex = len(self.ciVertices)
            self.ciVertices[str_coord] = nodeIndex
            self.icVertices[nodeIndex] = coord
            return nodeIndex   
        else:
            nodeIndex = self.ciVertices[str_coord]
            return nodeIndex   
   
    def getUniqueRoadsSectionsNodes(self):
        result = []
        for k, v in self.edges.items():
            nbConnectedVertices = len(v)
            if 2 != nbConnectedVertices:
                result.append({ "the_geom": self.icVertices[k], "nb_connections": nbConnectedVertices })
        return result

    def __getNextVertex(self, prev, curr):
        succ = self.edges[curr]
        if 2 == len(succ):
            if (prev == succ[0]) and not (prev == succ[1]):
                return succ[1]
            elif (prev == succ[1]) and not (prev == succ[0]):
                return succ[0]
        return None

    def __burnEdge(self, idx1, idx2, burnedEdges):
        minIdx = min(idx1, idx2)
        maxidx = max(idx1, idx2)
        if burnedEdges.has_key(minIdx):
            burnedEdges[minIdx].add(maxidx)
        else:
            burnedEdges[minIdx] = set({ maxidx })

    def __buildRoadSection(self, vertexIndex, nextVertexIndex, burnedEdges):
        result = []
        
        prevIdx = vertexIndex
        result.append(self.icVertices[prevIdx])
        currIdx = nextVertexIndex
        result.append(self.icVertices[currIdx])
        self.__burnEdge(prevIdx, currIdx, burnedEdges)
        
        nextIdx = self.__getNextVertex(prevIdx, currIdx)
        while nextIdx is not None:
            result.append(self.icVertices[nextIdx])
            prevIdx = currIdx
            currIdx = nextIdx
            self.__burnEdge(prevIdx, currIdx, burnedEdges)

            if (nextIdx == vertexIndex):
                # current road section is a loop, stop the process
                nextIdx = None
            else:
                nextIdx = self.__getNextVertex(prevIdx, currIdx)            
            pass
        
        return result
    
    def getUniqueRoadsSections(self):
        distance = QgsDistanceArea()
        distance.setEllipsoidalMode(True)

        result = []

        burnedEdges = dict()
        for vertexIndex in self.edges.keys():
            nbConnectedVertices = len(self.edges[vertexIndex])
            if 2 != nbConnectedVertices:
                # current vertex is a 'boundary' of a 'road section'
                for nextVertexIndex in self.edges[vertexIndex]:
                    minIdx = min(vertexIndex, nextVertexIndex)
                    maxIdx = max(vertexIndex, nextVertexIndex)
                    if not (burnedEdges.has_key(minIdx) and (maxIdx in burnedEdges[minIdx])):
                        geom = self.__buildRoadSection(vertexIndex, nextVertexIndex, burnedEdges)
                        result.append({ "the_geom": geom, "distance": distance.measureLine(geom) })
        return result

    def remDoubles (self,seq):
        
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not(x in seen or seen_add(x))]

    def ChangeEdge(self, edgeDict):
        NewEdge = []
        FinalEdge = {}
        for edge in edgeDict.itervalues():
            NewEdge.append(self.remDoubles(edge))
        i=0
        for k in edgeDict.iterkeys():
            FinalEdge[k]= NewEdge[i]
            i+=1
        return FinalEdge

    def get_Intersections (self, divtroncon):
        NewEdges = self.ChangeEdge(self.edges)
        result = []
        bissResult=[]
        buffResult =[]
        final = []
        r = []
        res = []
        k= []
        j=0
        for vertexIndex in NewEdges:
            nbConnectedVertices = len(NewEdges[vertexIndex])
            if 2 < nbConnectedVertices:         
                r.append({ self.icVertices[vertexIndex] : [self.icVertices[nextVertexIndex] for nextVertexIndex in NewEdges[vertexIndex]]}) # if self.icVertices[nextVertexIndex] not in r[self.icVertices[vertexIndex]    
                k.append(self.icVertices[vertexIndex])
        i=0
        dividedList=[] 
#        print "R", r
        for intersectionDict in r:
#            for kk in k:
                
#            print "INTERSECTIONDICT", intersectionDict
            
            dividedList.append({"intersection":k[j], "divided edges":self.divideTroncon(divtroncon, intersectionDict)})
            j+=1
#        print " FINAL DIVIDED LIST", dividedList
#        print "dividlist", dividedList, "LEN", len(dividedList)   
        for dividedDict in dividedList:
#            print "divid dict", dividedDict
            
#            lenb = len(self.createSeriesOfAngles(dividedDict['intersection'],dividedDict['divided edges']))# == NB OF ATTRIBUTES !!!
            
            result.append(self.createSeriesOfAngles(divtroncon, dividedDict['intersection'],dividedDict['divided edges']))
            for dict in result:
                print len(max(dict))
#                print "angle",AngleDict
#                print "substracted", self.substract(self.__assess(AngleDict))
#                result.append({"the_geom": k[l], "distance" : str(m), "angles" : str(self.substract(self.__assess(AngleDict)))[1:-1]})
                
#                final.append(self.makeManyAttributes(lenb, k[l], str(self.substract(self.__assess(AngleDict)))[1:-1], m))
# WE WANT ({"the_geom" : k[l], "angle(m) : a, "angle(m+m)":b...}) 
                # "distance":str(m),

#            self.IterAngles(dividedDict, l, k[j])    


#            print "INTERSECTION DICT", intersectionDict 
#        print "DIVIDEDLIST", dividedList
#            if self.substract(self.__assess(intersectionDict))[0] < 1.0 :
#                pass
#            if self.substract(self.__assess(intersectionDict)) is not None:
#                if len(self.substract(self.__assess(intersectionDict))) >2:
#            else:
#                self.intersectionBuffer(intersectionDict)
            
#            result.append({"the_geom": k[j], "angle at distance n": str(self.substract(self.__assess(self.createSeriesOfAngles(dividedDict['intersection'],dividedDict['divided edges']))))[1:-1]}) #assess(buffer(intersectionDict))
#            bissResult.append({"the_geom": k[i], "bissectrices":self.bissec(self.__assess(intersectionDict))})
#            buffResult.append({"the_geom":k[i], "buffer":self.buffer(intersectionDict)})
#            i+=1        

#        for resDict in result:
#            if resDict['angles']!= 'on':
#                final.append(resDict)
#        print "BUFF: \n",buffResult
#        print "BISSEC: \n",bissResult
#        print "FINAL RESULT", result
        return result
        


    def makeManyAttributes (self, len, k, AngleDict, m):
        
        result = []
        distance = {}
        tracker =[]
#        print "AngleDict", AngleDict
#        print "len", len
#        print "k", k
#        print "m", m
        distance['the_geom']=k
        for i in range(len):
            
            distance['distance%d' %m]=AngleDict

            if distance['the_geom'] not in result:
                result.append(distance)
#        print distance
#        for intersection in k:
#            result.append(distance)
#            result['the_geom']=intersection
#        print "MAKEMANY RESULT", result
        
    def createSeriesOfAngles(self, divtroncon, key,values):
        """
          Return n times the nth number of every list in `values`,
          in a list of dictionaries.
        """
        final={'the_geom':key}
        intersect_list = []
        longest = max(map(len,values))
        i=1
        j = int(i)*int(divtroncon)
        for n in range(longest):

#            print "JJJJJJJ", j
            
            # get the nth value if there is one, or just the last value
            nth_values = [l[n] if n<len(l) else l[-1] for l in values]
            final.update({'at distance %s'%(str(int(i)*int(divtroncon))): str(self.substract(self.assessor(key, nth_values)))[1:-1]})
            i+=1
            intersect_list.append({key:nth_values})

        print "FINAL", final
#        print "INTERSECT_LIST", intersect_list
#        self.assessor(final)
        return final
#        return intersect_list
        
            
    def IterAngles(self, dividedDict, l, k):
        segDict={}

#        print "dividedlist", dividedDict
        seglist = []
        for anglist in dividedDict['divided edges']:
            a = 0
            for segment in anglist:    
                seglist.append(anglist[a])
            a+=1
        
        segDict[k]=seglist
        
#            for segments in Dict['divided edges']:
#                seglist.append(segments[2])
        #        print "segments",segments
        #        for point in segments:
#            segDict[k]=seglist
            
#        print "SEGDICT", segDict
#        print "seglist",seglist
        return segDict
            
    def substract(self,Anglist):
        result = []
        i=0
        j=1    
        for angle in Anglist[:-1]:
            if Anglist[j]-Anglist[i]!= 0:            
                result.append(Anglist[j]-Anglist[i])
                i+=1
                j+=1
        result.append(Anglist[0]+(360-Anglist[-1]))
        if len(result) >2:
            return result

    def __assess(self, intersectionDict):
#        print "IntD",intersectionDict
        result = []
        for key,values in intersectionDict.iteritems():
            i = 0
            for pointInQuestion in values:
                point = (values[i][1]-key[1]),(values[i][0]-key[0])
                angle = self.angle_between(point, (0.0,1.0))
                result.append(angle)
                result.sort()
                i+=1
        return result

    def assessor(self, key, nth_values):
#        print "Nth", nth_values
        result = []
        i=0
        for PointInQuestion in nth_values:
                point = (nth_values[i][1]-key[1]),(nth_values[i][0]-key[0])
                angle = self.angle_between(point, (0.0,1.0))
                result.append(angle)
                result.sort()
                i+=1
#        print 'RESSSS', result
        return result
    
            
    def angle_between(self,p1, p2):
        ang1 = np.arctan2(*p1[::-1])
        ang2 = np.arctan2(*p2[::-1])
        return np.rad2deg((ang1 - ang2) % (2 * np.pi))

    
    def createPointsAt(self, distance, geom, intersection ): #intersection = PointOfInterest
#        print "CREATEPOINTSAT start"
#        print "INTERSECTION", intersection
#        print "GEOM", geom, type(geom)

        feats = []  
        result = []
        final = []
        line = QgsGeometry.fromPolyline(geom)
#        print "LINE", line, type(line)
        if distance > line.length():
#            print "Line Too Short!", line.length()
            result=geom
    
        length = line.length()
        currentdistance = distance
        ends = geom
        end1=ends[1]
        end2=ends[-1]
#        print "Dist 1", currentdistance

        i=2
        if end2 == intersection:
#            print "REVERSED!"
            geom.reverse()
#        result.append(geom[0])
        
        while currentdistance < length: 
            point = line.interpolate(currentdistance)
            result.append(point.asPoint())
            
            currentdistance = currentdistance + distance
#            print "Dist %d" %(i), currentdistance
            i+=1
#            fet = QgsFeature()
#            fet.setAttributeMap( { 0 : currentdistance } )
#            fet.setGeometry(point)
#            feats.append(fet)
#        result.append(line.asPoint())
#        final.append({intersection:result})
        if distance < length:
            result.append(geom[-1])
#        print "RESULT", result
        return result
        
    
    def divideTroncon (self, divtroncon,intersectionDict):
        result = []
        SectionsInIntersection = []

#        print "GetUniqueSections", self.getUniqueRoadsSections()
#        print "ORIGIN", origin
        for UniqueSection in self.getUniqueRoadsSections():
            for key in intersectionDict.keys():
#                print "key", key
#                print "Uniquesection", UniqueSection['the_geom']
                
#                print 'UniqueSection[the_geom]', UniqueSection['the_geom'][0], type([UniqueSection['the_geom'][0]])
#                print 'intersectionDict.keys()', intersectionDict.keys()[i], type(intersectionDict.keys())
            
                if UniqueSection['the_geom'][0] == key:
                    SectionsInIntersection.append(UniqueSection['the_geom'])
                elif UniqueSection['the_geom'][-1] == key:
                    UniqueSection['the_geom'].reverse()
                    SectionsInIntersection.append(UniqueSection['the_geom'])
            Intersection = {key:SectionsInIntersection} 
#            print "INTERSECTION", Intersection       
#            if intersectionDict.keys() in UniqueSection['the_geom']:
#            print "RSofUnique:", UniqueSection

        for values in Intersection.values():
#                print "VALUES", values
            for line in values:
                result.append(self.createPointsAt( divtroncon, line, key))
#            print "Section", Section

#        print "DIVIDE RESULT", result
        return result
#        self.createPointsAt(5, geom, self.edges.keys())
#        print "the_geom divided",geom.asPolyline(), type(geom)
 