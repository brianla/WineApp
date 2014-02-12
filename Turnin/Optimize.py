class Optimize:
  def __init__(self, clusters):
		self.clusters = clusters
		self.numberOfClusters = len(clusters)

	def optimizeEps(self, minpts):
		desiredNumberOfClusters = 2 * math.sqrt(totalPoints)

		if self.numberOfClusters < desiredNumberOfClusters:
"""
	With minpts so fixed, loop through the clusters:
	if the # of clusters is < desiredNumberOfClusters, then
	the clusters eps is too large.

	Find out how many more points are in the cluster than there should
	be (minpts), then find that # of points where are at a maximal
	distance from one another
	Take the avg distance of these # points, and subtract this from
	the avg distance of the remaining minpts points.
	Compute eps - discovered value
	Very much a work in progress, considering a different approach now

	Do this for all clusters
	Avg this
	new eps  = eps - avg

	Do this for all of the clusters.
"""
	#dist (A, B) and (B, A) is equilivent. Also, I will count both boths for the below
	def maximalDistances(self, cluster):
		pairwiseDistance = []
		size = len(cluster.points)
		index = 0
		subIndex = 0
		currPoint = None
		otherPoint = None

		while index < size:
			currPoint = cluster.points[index]
			subIndex = index + 1

			while subIndex < size:
				otherPoint = cluster.points[subIndex]
				pairwiseDistance.append(currPoint.distance(otherPoint))
				subIndex += 1

			index += 1

		pairwiseDistance.sort()
		return pairwiseDistance

	def excessRadius(self, excessPoints, maxDistances):
		index = len(maxDistances) - 1
		count = 0
		stop = math.floor(excessPoints / 2) #if this is odd, I could try taking the next largest distance and cutting it in half if the results seem they need the fix
		total = 0.0

		while index > -1 and count < excessPoints:
			total += maxDistances[index]

		return total / excessPoints

	def properRadius(self, excessPoints, maxDistances):
		totalProperPoints = len(maxDistances) - excessPoints
		index = totalProperPoints
		total = 0.0

		while index > -1:
			total += maxDistances[index]

		return total / totalProperPoints

	def calculateExcessRadius(excessPoints, maxDistances, cluster, eps):
		difference = self.excessPoints(excessPoints, maxDistances) - self.properRadius(excessPoints, maxDistances)

		return eps - difference

	def clustersTooLarge(self, minpts, eps):
		numberOfPointsInCluster = 0
		excessPoints = 0
		total = 0.0

		for cluster in self.clusters:
			numberOfPointsInCluster = len(cluster.points)
			excessPoints = numberOfPointsInCluster - minpts #may be nagative. That's fine if it is
			maxDistances = self.maximalDistances(cluster)
			total += self.calculateExcessRadius(excessPoints, maxDistances, cluster, eps)

		return total / self.numberOfClusters #brand new eps

	def clustersTooSmall(self, minpts, eps):
		numberOfPointsInCluster = 0
		pointsDeficit = 0
		total = 0.0

		for cluster in self.clusters:
			numberOfPointsInCluster = len(cluster.points)
			pointsDeficit = minpts - numberOfPointsInCluster
			maxDistances = self.maximalDistances(cluster)
			total += self.calculateExcessRadius(excessPoints, maxDistances, cluster, eps)
