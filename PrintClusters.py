#from Cluster import *

class PrintClusters:
	def __init__(self):
		self.blah = None

	def printToTerminal(self, clusters):
		print "Number of Clusters: %s" % str(len(clusters))
		for cluster in clusters:
			self.printCluster(cluster)
			
	def printCluster(self, cluster):
		print "ClusterID: %s" % str(cluster.clusterID)
		print "CSO:"
		self.printPoint(cluster.CSO)
		print "Cluster's Points:"
		self.printPoints(cluster.points)

	def printPoints(self, points):
		print "\tNumber of Points in the Cluster: %s" % str(len(points))
		for point in points:
			self.printPoint(point)

	def printPoint(self, point):
		print "\tClassed: %s" % str(point.classed)
		print "\tID: %s" % str(point.ID)
		print "\tDensity: %s" % str(point.density)
		print "\tPoints Values: "
		self.printValues(point.values)

	def printValues(self, values):
		print "\t\tNumber of Values in the Point: %s" % str(len(values))

		for value in values:
			self.printValue(value)

	def printValue(self, value):
		print "\t\t%s" % str(value)

	def printListOfNodes(self, listOfNodes):
		for node in listOfNodes:
			self.printNode(node)

	def printNode(self, node):
		print "\tDistance: %s" % str(node.distance)
		print "\tPoint:"
		self.printPoint(node.point)
