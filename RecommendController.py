"""Recommender system processing module
"""

from Classes import *
from InstantiationValidation import *
from UserModelAccess import *
from InventoryModelAccess import *
from RecommenderModelAccess import *
import Globals
from Cluster import *
from random import *

def updateClusters():
  ##print "Just now in updateClusters"
  eps = 0.2
  minpts = 9
  ##print "Just before cluster updater"
  points = convertWinesToPoints()
  if isinstance(points,basestring):
    return "Error found"
  factory = ClusterBuilder(eps, minpts, points)
  ##print "Starting constructing"
  factory.constructClustersForPoints()
  updateDatabase()
  ##print "Finish constructing"
  
def updateDatabase():
  print "Getting in the method at all"
  print "Attempting to change the DB values:"

  try:
    for point in self.pointsList:
      dbSetClusterID(point.ID, point.clusterID)
      dbSetCSOByWineID(point.ID, point.isCSO)
  except:
    ex, ex_type, tb = sys.exc_info()
    print ex
    print ex_type
    traceback.print_tb(tb)
    del tb

    print "Finished updating the database"

def convertWinesToPoints():
  ###print "Converting the wines to points Now"
  wines = dbGetAllWines()
  if wines == None:
    return "Error getting wines"
  else:
    wines = wines[0]
  points = []

  for wine in wines:
    if wine.wineID != 0:
      points.append(toPoint(wine))
    
  #print "Finished converting the wines"

  return points

def getUserShelves(user):
  return dbGetUserShelves(user)


def createChannel(user, channelName, seeds):
  """Create a recommendation channel
  
  Arg:
    UserInfo user: UserInfo object representing the user
    string channelName: The name of the channel
    list seeds: List of wineIDs
  """
  return dbCreateChannel(user, channelName, seeds)
  

def editChannel(recommender, channelName):
  """Change the name of a channel.

  Arg:
    Recommender recommender: Recommender 
    string channelName: Name to change to
  """
  return dbEditChannel(recommender, channelName)

  
def removeChannel(recommenderID):
  """Remove a recommendation channel
  
  Arg:
    int recommenderID: The id of the channel.
  """
  return dbRemoveChannel(recommenderID)
  
  
def addSeeds(recommenderID, seeds):
  """Add seeds to a channel.
  
  Args:
    int recommenderID: The id of the channel
    list seeds: A list of wineIDs specifying seed wines.
  """
  return dbAddSeeds(recommenderID, seeds)

def getSeeds(recommenderID):
    return dbGetSeeds(recommenderID)
  
  
def removeSeeds(recommenderID, seeds):
  """Remove seeds from a channel.
  
  Args:
    int recommenderID: The id of the channel
    list seeds: A list of wineIDs to remove as seeds.
  """
  return dbRemoveSeeds(recommenderID, seeds)      


def recommend(recommenderID, numWines):
    """Recommend wines to user based on Wine seed
  
    Args:
    recommenderID: Channel ID
    int numWines: number of wines to recommend at once
        
    Return:
    list: List of close Wine objects
    """
    print "Starting recommendations getting"
    history  = dbGetRecommenderHistory(recommenderID)

    if history[0] == None:
    	return(None, (None, ["Error getting history"]))
    else:
    	history = history[0]
    	
    seeds = dbGetSeeds(recommenderID)
    csos = dbGetCSOs()
    print "DEBUG: seeds = " + str(seeds)

    if not seeds[0] or seeds[0] == None:
        return (None, (None, ["Error getting seeds"]))
    else:
        seeds = seeds[0]
    	
    if not csos[0] or csos[0] == None:
    	return (None, (None, ["Error getting csos"]))
    else:
    	csos = csos[0]
    
    print "Starting seeds thing"
    ourSeed = seeds
    #if more than one seed is given
    if len(seeds) > 1:
        print "len seeds > 1"
        randomSeed = randrange(0,len(seeds))
        ourSeed = seeds[randomSeed]
    else:
        print "len seeds <= 1"
        ourSeed = seeds[0]

        #print "DEBUG: Found ONE seed"
        #print "DEBUG: seeds[0] = " + str(seeds[0])
        #print "DEBUG: Seed wine ID: " + str(seeds[0].wineID) + \
        #             " Name: " + str(seeds[0].wineName) + \
        #              " Winery: " + str(seeds[0].winery) + \
        #              " Vintage: " + str(seeds[0].vintage)

        
        
        #convert the cso Wines to points
    csoPoints = []
    for cso in csos:
        csoPoints.append(toPoint(cso))
        #print "DEBUG: CSO's ID is: " + str(cso.wineID) +\
        #     " Name: " + str(cso.wineName)
    
    #convert the wine's attributes to a point    
    p = toPoint(ourSeed)

    wines = []
    n = 0

    print "starting wine loop"
    while not wines:
        print "Wine loop iteration"
        
        if n > len(csoPoints):
            # We have recommended all the wines in the database
            return (None, (None, ["Stop asking for more wines!"]))

        cluster = getNthClosestCSO(n, p, csoPoints)
        #print "Getting the " + str(n) + "th closest cso: " + str(cluster)
        #clusters is a sorted list of cso's point right now

        realWine = dbGetWineByID(cluster.pointID)
        
        if realWine[0] == None:
            return (None, (None, ["Error getting wine"]))
        else:
            realWine = realWine[0]

        #print "DEBUG: Cluster's ID: " + str(realWine.wineID) +\
        #      " Name: " + str(realWine.wineName) +\
        #      " Winery: " + str(realWine.winery) +\
        #      " Vintage: " + str(realWine.vintage)
                
        #getting wines belonging to the selected cluster
        clusterWines = dbGetWinesInCluster(realWine)
        ##print "DEBUG: Cluster wines: " + str(clusterWines)
        if clusterWines[0] == None:
            return (None, (None, ["Error getting wine cluster"])) 
        else:
            clusterWines = clusterWines[0]
            
        #convert clusterWines to points
        clusterPoints = []
        for wine in clusterWines:
            clusterPoints.append(toPoint(wine))

        winesWithDistance = []
        for point in clusterPoints:
            
            tempWine = dbGetWineByID(point.pointID)
            if tempWine[0] == None:
                return (None, (None, ["Error getting wine"]))
            else:
                tempWine = tempWine[0]
            wwd = WineDistance(tempWine, p.distance(point))
            winesWithDistance.append(wwd)
        winesWithDistance.sort(key = lambda wineDistance: wineDistance.distance)
            #if DEBUG:
            #print "1 wine: " + str(winesWithDistance[0].wine.wineID)
        #print "Distance for first wine: " +str(winesWithDistance[0].distance)
        #print "2 wine: " + str(winesWithDistance[1].wine.wineID)
        #print "Distance for second wine: " +str(winesWithDistance[1].distance)
        #print "3 wine: " + str(winesWithDistance[2].wine.wineID)
        #print "Distance for second wine: " +str(winesWithDistance[2].distance)
        #print "4 wine: " + str(winesWithDistance[3].wine.wineID)
        #print "Distance for second wine: " +str(winesWithDistance[3].distance)
        #print "5 wine: " + str(winesWithDistance[4].wine.wineID)
        #print "Distance for second wine: " +str(winesWithDistance[4].distance)


        notEnoughWines = True

        for wwd in winesWithDistance:
          wines.append(wwd.wine)

        while notEnoughWines:
            print "notEnoughWines loop"
            wines.extend(getTopNRecommended(numWines, wines))
            checkHistory(history, wines)
            if len(wines) > numWines:
                notEnoughWines = False
                wines = wines[:numWines]
                for wine in wines:
                    rh = RecommenderHistory(None,recommenderID,wine.wineID,None,0)
                # Does not check if recommender history was added properly
                    dbAddRecommenderHistory(rh)
                return (wines, None)

            else:
                n += 1
                break
    print "returning"
    return (wines, None)
         
                


def getRecommender(recommenderID):
    """Get a recommender object.

    Arg:
        int recommenderID: ID of the recommender
    """
    return dbGetRecommender(recommenderID)


def getRecommendHistory(recommenderID):
    """Preprocess retrieval of some number of wines recommended in the past.

    Args:
        int recommenderID: ID of the recommender to get history from
        int numWines: Number of wines from history to return

    Return:
        list of wines
    """
    hists = dbGetRecommenderHistory(recommenderID)
    if hists[0] == None:
        return (None, hist[1])
    else:
        hists = hists[0]

    # Sort histories by recent time and get numWines of them
    hists.sort(key = lambda hist: hist.timestamp, reverse = True)
    #hists = hists[:numWines]

    wines = []
    for hist in hists:
        wine = dbGetWineByID(hist.rh_wineID)
        if wine[0] == None:
            return (None, wine[1])
        else:
            wine = wine[0]

        wines.append(wine)

    return (wines, None)
  
  
def randomWine(numWines):
    """Retrieve a random set of wines
      
        Call DataAccess layer to retrieve a random set of wines.
        Args:
        int numWines: number of random wines to get
            
        Return:
        list: A list of random Wine object
    """
    lis = []
    for i in range(numWines):
        lis.append(dbRandomWine()[0])
    return lis

def checkHistory(history, wines):
    """ Routine for recommend() that checks the list of previously
        recommended wines for the user
            
        
        Args:
        list RecommenderHistory: list of previously recommended wines
        list Wine : list of wines with associated distance to seed
    
        Return:
        None
    """
    
    #compare to the wines to be recommended
    #O(n^2), but hopefully won't significantly impact overall performance
    print "Beginning to check the history"
    for h in history:
        for wine in wines:
            if h.rh_wineID == wine.wineID:
                wines.remove(wine)

def getTopNRecommended(numWines, wines):
    """ Routine for recommend() that checks the list of previously
        recommended wines for the user
        
        
        Args:
        int numWines: number of wines to show to the user
        list wines: list of wine objects
        
        Return:
        list: A smaller list of wine objects
    """
    mylist = []
    if numWines < len(wines):
        for i in range(numWines):
            mylist.append(wines[i])
    else:
        for i in range(len(wines)):
            mylist.append(wines[i])
    return mylist

def getNthClosestCSO(n, p, clusters):
    """Find the CSOs closest to this wine
    
        Calculate a wine point's distance to the characteristic point of each cluster
    
        Args:
        Point p: Point converted Wine object representing the input wine
        list clusters: list of Points, each representing a CSO
    
        Return:
        points[n]: Point object of the nth closest CSO
    """
    
    pointsWithDistances = []
    for point in clusters:
        pointsWithDistances.append((point, p.distance(point)))
    #consider changing to alternate syntax
    pointsWithDistances.sort(key=lambda pwithd: pwithd[1])
    points = [x[0] for x in pointsWithDistances]
    return points[n]

def getCandidateWines(attrs):
    """ Gets a list of candidate wines from the database :D """
    
    return dbShelfWineCandidates(attrs)



def toPoint(wineObject):
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
            
            
    newPoint = Point(wineList, wineObject.wineID, wineObject.varietal, wineObject.wineType)
    return newPoint


class WineDistance:
    """ Object containing a wine object and its corresponding distance to the seed
        Need this to be able to sort wines by distance, using the sorted() function
        Instance Variables:
        Wine wine: a wine object
        float distance: distance from this wine to the closest seed
    """
    def __init__(self, wine, distance):
        self.wine = wine
        self.distance = distance




