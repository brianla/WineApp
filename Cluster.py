#!/usr/bin/env python

import os
import random
import math
from PrintClusters import *
import copy
from collections import *

"""
	The cluster class!

	 Note: Calculate out the densities of each central point in a cluster and 
	subtract off the range. Find the maximal for each cluster and use that as 
	the CSO, and sort this prior to use in the actual clustering system.

	Notes and Definitions: BTW: These are pretty much my typed up notes from reading
	the paper about this particular implementation, so (hopefully) this provides
	an accessible resource for figuring out what this class is supposed to do =)

	Eps neighborhood: N(eps)
	The set of all points wihin eps (the radius of a cluter) such that the
	distance between any two points in <= Eps (can be thought of like a radius)
	Ie: Its the group of all points that are chillin within eps of one another =)

	Types of Points: You have your core points, then you have your border points.
	The core points are well within eps of the cluster, and the border points are
	the ones that are just barely within eps of the cluster. 

	Directly Density Reachable (DDR): This is with respect to the global values of
	eps and minpoints.
	A point p is DDR from a point Q if p is in the same neighborhood as q and
	if the neighborhood of q has at least as many points as minpoints.
	IF you got both, then p is DDR to Q wrt to minpts and eps.
	Note: This is NOT in general symmetric! Works for core points, but not a 
	core point and a border point!
	Density reachable:
	A point p is DR from a point Q if there exists points P1...PN such that
	P1 = Q, PN = P, and PI+1 is Directly density reachable fron PI.

	Density connected: There exists a point o such that both p and q are
	DR from o.

	Main Ideas on the clustering:
	A cluster is any subset of the set of points in the database. 
	For any two points in a cluster (P, Q) 
	A) If P is in the cluster and Q is density reachable from P, the Q
	is in the cluster
	B) A pairs of points in a cluster are density-connected
	
	Noise: Any points in the database that are not in any of the clusters

	Note: eps and minpoints would be awesome to specify manually, and perhaps
	we can select optimal parameters for our dataset on the presentation, but
	there are heuristics for generating them on the fly, and I have gone
	ahead and used said methods =)

	The algorithm:
	Start off with a random point P, then find all points density-reachable from P.
	If P ends up being a core pointm that collection becomes a cluster. If P is a
	border point, no other points are density reachable to P, and hence P is marked
	(for now) as noise. So, move on to the next point.
	Note: During our clustering, two clusters may end up being merged together according to the
	def of a cluster.

	The distance between two clusters is the smallest distance between a point in one
	and a point in another

	Note: Clusters may themselves contain clusters! Recursive in that case

	setOfPoints.regionQuery returns the list of points that are in the eps neighborhood of it.
	This is where the m-trees come in =)

	If a cluster is close to another, a point in one may be reachable from the other. In that case,
	whichever cluster that point was orginally assigned to is the cluster it will remain in

	heuristic for determining eps and minpoints:

	Let d represent the distance from a point p to its k nearest broskies. This means that there are K + 1 points
	for pretty much all points p.
	There are more if several points lie exactly the same distance apart. Changing k does not change d much, except
	if all the points p lie on a straight line (rare).
	We can also sort all the points in the database by their d values. Doing so gives us clues onto the distribution of 
	the points in the database. For a arbitary point P, eps would be the D and minpoints would be K. The cluster in D that
	has the maximal k-dist value whilst being very thin would represent the optimal value for for eps and minpoints.
	If you graphed the data, this optimal values would be the first valley in the sorted graph. Hard to detect algorithmatically,
	but easy to spot visually.
	#pointsList is the list of points sorted according to density
	#check: if the CSO's that are produced generate clusters with CSO's
	#still in this same sorted order

	For later reference: you can make your own simple map with an object
	by having a int field (in custom object) which will store an item's index into the map
	array.
	Then, use lazy deletion when removing items and maintain a queue (implemented as a linked list)
	which keeps track of the open positions in the array. If anything gets removed, place that index
	into the queue, and use that position for subsequent inserts. The array itself should be
	implemented as an arraylist, so it can be dynamically updated for size. Should accept an inital size
	This runs very, very fast, is very, very simple. Optains perfect hashing everytime as well.
	Does require a tight coupling between the map and the object it will be mapping.
	ArrayList:
	Once out of space, alloc an array of 2*currSize of the currentType, and assign it totalPoints
	a pointer to an internal balanced btree. That should be a pretty short tree, so lookups in 
	it will be pretty fast, does not have to copy all of the array positions over again. 

"""

c_typeScalar = 0.1
c_varietalScalar = 0.1

class Point:
	def __init__(self, values, pointID, varietal, designation):
		self.values = list(values) 
		self.classed = -3 #initally unclassified. Vals: -3 Unclassified -2 Classified (as Noise) -1 (Visited, but still Unclassified)  >= 0: classified in cluster with index in cluster = self.classed
		self.pointID = pointID #should be the wineID
		self.clusterID = None
		self.density = 0
		self.pointType = designation #string
		self.varietal = varietal #string
		self.isCSO = 0
		self.nearbyPoints = []
		self.nearbyDistances = []
		self.key = -1

	def distance(self, other):
		selfSize = len(self.values)
		sub = 0.0
		total = 0.0

		for index in range(selfSize):
			sub = self.values[index] - other.values[index]
			sub = sub * sub
			total += sub

		total += 0 if self.pointType == other.pointType else c_typeScalar
		total += 0 if self.varietal == other.varietal else c_varietalScalar

		return total

	def appendPointAndDistance(self, point, distance):
		self.nearbyPoints.append(point)
		self.nearbyDistances.append(distance)

	def classedToString(self):
		if self.isUnclassified() == True:
			return "Point %s is unclassified" % self.pointID
		elif self.isNoise() == True:
			return "Point %s is classified as noise" % self.pointID
		elif self.isClustered() == True:
			return "Point %s is classified in a cluster with clusterID: %s at position: %s" % (self.pointID, self.clusterID, self.classed)
		elif self.alreadyVisited() == True:
			return "The node was visited but not accepted. That's not good. %s!" % self.pointID
		else:
			return "classed as the CSO"

	def isUnclassified(self):
		if self.classed == -3:
			return True

		return False

	def alreadyVisited(self):
		if self.classed == -1:
			return True

		return False

	def isNoise(self):
		if self.classed == -2:
			return True

		return False

	def isClustered(self):
		if self.classed >= 0:
			return True

		return False

	def isClusteredAtIndex(self):
		if self.isClustered == True:
			return self.classed
		else:
			return -1

	def isNowClustered(self, withIndex, inClusterWithID):
		self.classed = withIndex
		self.clusterID = inClusterWithID

	def isNowNoise(self):
		self.classed = -2

	def isNowVisited(self):
		self.classed = -1

	def isCSO(self):
		return isCSO

	def __str__(self):
		toString = []
		toString.append(self.classedToString())
		toString.append("\nDensity: %s\n" % self.density)
		toString.append("pointID: %s\n" % self.pointID)
		toString.append("pointID type: %s" % type(self.pointID))

		toString.append("\nValues: \n")

		for value in self.values:
			toString.append("\t%s" % value)
			toString.append("\n")

		return ''.join(toString)

	def __hash__(self):
		return self.pointID
	"""
	< 1 this point is < otherPoint
	= 0 this point = otherPoint
	> 1 this Point is > otherPoint
	"""
	def compare(self, otherPoint):
		thisSize = len(self.values)

		if thisSize == len(otherPoint.values):
			#That's an error otherwise
			total = 0
			for index in range(thisSize):
				total = total + compareComponent(self.values[index], otherPoint.values[index])

		return total
				
class Cluster:
	def __init__(self, ID):
		self.points = []
		self.clusterID = ID
		self.totalPoints = 0
		self.CSO = None

	def addPoint(self, point):
		point.isNowClustered(self.totalPoints, self.clusterID)
		self.totalPoints += 1
		self.points.append(point)

	def setCSOAndAddToList(self, theCSO):
		self.CSO = theCSO
		theCSO.isCSO = 1
		theCSO.classed = -4

	def __str__(self):
		toString = []

		toString.append("ClusterID: %s" % self.clusterID)
		toString.append("\nThis is cluster %s, which has %s total points" % (self.clusterID, self.totalPoints))
		toString.append("\nCSO is %s\n" % self.CSO)

		return ''.join(toString)

class QueueSet:
	def __init__(self):
		self.index = 0
		self.length = 0
		self.queue = deque()

	def doesExist(self, item):
		if item.key == -1:
			return False
		else:
			return True

	def hasNext(self):
		if self.length != 0:
			return True
		return False

	def append(self, item):
		if self.doesExist(item) == False:
			item.key = self.index
			self.index += 1
			self.length += 1
			self.queue.append(item)

	def addItems(self, items):
		for item in items:
			self.append(item)

	def popLeft(self):
		self.length += -1
		return self.queue.popleft()
		
	def __len__(self):
		return self.length

class ClusterBuilder:
	def __init__(self, eps, minpts, points):
		self.totalPoints = len(points)
		self.clusters = []
		self.pointsList = points #will point to the list of points passed in
		self.eps = eps;
		self.minpts = minpts
		self.clusterLength = 0
		self.noisePoints = set()

	def buildEpsNeighbors(self):
		#print "Started building the eps neighbors"
		index = 0
		while index < self.totalPoints:
			self.epsNeighborsForPoint(index)
			index += 1

	def calcDensityForPoint(self, currPoint):
		totalDensityForCurrPoint = 0
		currListSize = len(currPoint.nearbyPoints)
		total = 0
		
		otherPointsIndex = 0
		while otherPointsIndex < currListSize:
			total += (self.eps - currPoint.nearbyDistances[otherPointsIndex])
			otherPointsIndex += 1

		currPoint.density = total

	def calcDensitiesForPoints(self):
		index = 0

		while index < self.totalPoints:
			self.calcDensityForPoint(self.pointsList[index])
			index += 1

	def epsNeighborsForPoint(self, currIndex):
		currPoint = self.pointsList[currIndex]
		otherPoint = None
		distance = None
		#avgDistance = 0

		otherPointsIndex = currIndex + 1

		while otherPointsIndex < self.totalPoints:
			otherPoint = self.pointsList[otherPointsIndex]
			distance = currPoint.distance(otherPoint)  
			#avgDistance += distance

			#print "The distance between point %s and %s is %s" % (currPoint.pointID, otherPoint.pointID, distance)

			if distance <= self.eps:
				#print "Distance was %s" % distance
				currPoint.appendPointAndDistance(otherPoint, distance)
				otherPoint.appendPointAndDistance(currPoint, distance)
			otherPointsIndex += 1

		#print "There was %s nearby" % len(currPoint.nearbyPoints)
		#print "There was %s nearbyDistances" % len(currPoint.nearbyDistances)


		#avgDistance = avgDistance / (self.totalPoints - currIndex)

		#print "The avg distance on the points compared for points %s was %s" % (currPoint.pointID, avgDistance)

	def addPointAsNoiseAndSoMark(self, point):
		point.isNowNoise()
		self.noisePoints.add(point)

	def makeCluster(self):
		theCluster = Cluster(self.clusterLength)
		self.clusterLength += 1 #Ensures each cluster gets a uniqueID, and conviently keeps a count on the length
		return theCluster

	def setAllAsVisited(self, points):
		for point in points:
			point.isNowVisited()

 	def expandCluster(self, currPoint, currCluster):
 		potentialClusterPoints = QueueSet()
 		potentialClusterPoints.append(currPoint)
 		 #since I sorted ng to density, the first point added here is the next most dense point

 		#print "There was enough points to start clustering. Number: %s" % len(potentialClusterPoints)
 		#Note: visited checks are not needed due to the aid of the set =)
 		while potentialClusterPoints.length != 0:
 			potentialPoint = potentialClusterPoints.popLeft()
 			#print "Got here"

 			#print potentialPoint

 			if len(potentialPoint.nearbyPoints) >= self.minpts:
 				potentialClusterPoints.addItems(potentialPoint.nearbyPoints)
 				#print "Added the items"
			if potentialPoint.isClustered() is False:
				currCluster.addPoint(potentialPoint)
			#print "Size of the queue at the end: %s" % potentialClusterPoints.length
 				
	def constructClustersForPoints(self):
		self.buildEpsNeighbors()
		
		self.calcDensitiesForPoints()
		self.pointsList.sort(key=lambda point: point.density, reverse=True)
		
		index = 0
		currPoint = None

		while index < self.totalPoints:
			currPoint = self.pointsList[index]

			if currPoint.isUnclassified() == True:
				if len(currPoint.nearbyPoints) < self.minpts:
					#print len(currPoint.nearbyPoints)
					#print "This one was less than minpts"
					currPoint.isNowNoise()
				else:
					#print currPoint.nearbyPoints
					#print "There was %s points nearby" % len(currPoint.nearbyPoints)
					cluster = self.makeCluster()
					self.expandCluster(currPoint, cluster)
					#print "After the return, there was %s many points in the cluster" % len(cluster.points)
					cluster.setCSOAndAddToList(currPoint)
					self.clusters.append(cluster)
			index += 1
		

	def __str__(self):
		toString = []

		for cluster in self.clusters:
			toString.append("Cluster %s is \n\t" % cluster)

		return ''.join(toString)
