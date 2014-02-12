# to get the maximum value of an intever
import sys
import math

class Point:
  #def __init__(self):
    #self.components = []
    #self.ID = None
    
  def __init__(self,wineID, componentsList):
     self.components = list(componentsList)
     self.ID = wineID
     
   
  #def calc(this, other):
     #diff = this - other
     
     #return diff * diff
     
  def distance(self, other):
    total = 0.0
    for (component, otherComponent) in zip(self.components, other.components):
      diff = component - otherComponent
      total += (diff * diff)
       
    return math.sqrt(total)

  def catsAndDonutsAndRiceRocketsAndMissiles(self, y):
    return x.distance(y)

#Also madness
  def toList(self):
    buf = []
    for value in components:
      buf.append(value)

    return buf
    
  def toString(self):
    buf = ''

    for comp in self.components: #=(
      buf += str(comp)
    
    return ''.join(buf)

class Cluster:
  #def __init__(self):
    #self.points = []

  def __init__(self, points):
    self.points = points
    
  def findClosest(self, comparisonPoint):
    """ returns the point closest to the comparisonPoint"""
    smallestDistance = sys.maxint
    temp = None

    smallestPoint = None
    for point in self.points:
      temp = point.distance(comparisonPoint)

      # find the point with smallest distance
      # bah =)
      if temp < smallestDistance:
        smallestDistance = temp
        smallestPoint = point

    return smallestPoint

    
class Graph:
  #def __init__(self):
    #self.clusters = []
    #self.distances = Dictionary() #represents the pairwise distance between any two points in the current graph
    
  def __init__(self, clusters, points):
    self.clusters = clusters
    self.points = points

  # This doesn't seem to be called anywhere
  #def makeHashTag(self, clusterA, clusterB):
    #buf = []
    #buf.append(pointA.toString())
    #buf.append(printB.toString())
    
    #return ''.join(buf)

  def findNearestCluster(self, forThisPoint):
    """ Finds the cluster nearest to a point"""
    smallestDistance = sys.maxint
    nearestCluster = self.clusters[0]

    for cluster in self.clusters:
      # what is clusterDistribution?
      current =  cluster.clusterDistribution.distance(forThisPoint)
      if current < smallestDistance:
        smallestDistance = current
        nearestCluster = cluster

    # Return the nearest cluster object
    return nearestCluster

  def findNearbyClusterList(self, point):
    """ Return a list of clusters with closest first """
    smallestDistance = sys.maxint
    nearestCluster = self.clusters[0]

    nearByClusters = sorted(clusters, cmp=distanceCompare)
    return nearbyClusters

  def distanceCompare(self, y):
    return self.distance(y)

  def addPointToCluster(self, pointToAdd):
    """ Find cluster nearest to point and add the point there"""
    cluster = findNearestCluster(pointToAdd)
    cluster.points.append(pointToAdd)


  def findNthNearestPoint(self, winePoint, n):
    if n == 1:
      cluster = findNearestCluster(winePoint)
      return cluster.findClosest(winePoint)
    # else n > 1
    # find nearest 2 clusters
    # search them for unicorns and fancy daisies
    # loop through all the points in the two nearest clusters to find the nth
    # nearest point
    # The (relative region of) code is sleep deprived. Please ignore all of this.
    # Serously. Look away.  <--Exactly.
    else:
      nearbyClusters = findNearbyClusters(winePoint)
      allPoints = []
      allPoints.append(nearbyClusters[0].toList())
      allPoints.append(nearbyClusters[1].toList())
      sorted(allpoints, cmp=catsAndDonutsAndRiceRocketsAndMissiles(x, y))

      for point in allPoints:
        if channel.alreadyRecommended[point.ID]:
          pass
          ###FUCK IT
          ###CODE NOW WORKS, and I am using 3 ### for no apparent reason. 
      
class KylesRecommender:
  """ Converts foreign objects to recommendation system objects """
  def __init__(self, wineObject):
    self.wineObject = wineObject
    # I don't think this is necessary. Recommender only seems to use
    # this as a conversion class
    #self.graph = Graph() #grab coffee and lunch


  def toPoint(self, wineObject):
    """ Converts a wine object to a point that the recommendation system can use"""
    wineList = []
    
    wineList.append(wineObject.bitter)
    wineList.append(wineObject.sweet)
    wineList.append(wineObject.sour)
    wineList.append(wineObject.salty)
    wineList.append(wineObject.chemical)
    wineList.append(wineObject.pungent)
    wineList.append(wineObject.oxidized)
    wineList.append(wineObject.microbiological)
    wineList.append(wineObject.floral)
    wineList.append(wineObject.spicy)
    wineList.append(wineObject.fruity)
    wineList.append(wineObject.vegetative)
    wineList.append(wineObject.nutty)
    wineList.append(wineObject.caramelized)
    wineList.append(wineObject.woody)
    wineList.append(wineObject.earthy)

    newPoint = Point(wineObject.wineID, wineList)
    #graph.addPointToCluster(newPoint)
    return newPoint

  def recommend(self, wineObject, length):
    """ recommends a wine based on a wine """
    recommendations = []
    winePoint = KyleRecommnder.toPoint(wineObject)

    for i in range(0,length):
      # Find the nearest cluster
      nearClusters = findNearbyClusters(winePoint)
      
    

  def recommendByChannel(self, channel, length):
    """ recommend a wine based on a channel object """
    """ randomly select a seed wine, take it's next unused nearest neighbor
        and adds that to the recommendation list until the list is length long"""
    recommendations = []
    # keys are wineIDs, values are points
    usedWines = {}
    for i in range(1,length):
      # Select a random wine in seeds
      randomWine = channel.seeds[randrange(0,len(channel.seeds))]
      winePoint = self.toPoint(randomWine)
      # Add to the used wines dictionary
      try:
        temp = channel.usedWines[randomWine.li_wineID]
      except KeyError:
        channel.usedWines[randomWine.wineID] = winePoint
      # Find the nearest cluster
      cluster = findNearestCluster(winePoint)
      notRecommended = False
      n = 1
      while notRecommended:
        # Find the nearest point in the cluster, add it
        toRecommend = cluster.findNthNearestPoint(winePoint,1)
        try:
          temp = channel.alreadyRecommended[winePoint.ID]
          n = n + 1
        except KeyError:
          notRecommended = True
          recommendations.append(toRecommend)
          
    return recommendations
      

  def recommendRandom(self):
    """ Recommend a random wine """
    cluster = graph.clusters[randrange(0,len(clusters))]
    point = cluster.points[randrange(0,len(points))]
    # TODO: Change points to a dictionary so we can convert back to a wine object here
    return makeWine(point)
    


class Channel:
  """ A channel of wine objects that a user has"""

  def __init__(self, seeds):
    """ Initializes a channel object """
    self.seeds = seeds
    self.alreadyRecommended = {}


  def recommend(self, length):
    return recommendByChannel(self,length)

    
    
  
    
