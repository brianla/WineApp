from flask import *
from Classes import *
from InstantiationValidation import *
import Globals
from sqlalchemy import *
import random
import sys
import datetime
import DBAccessConnection


def dbGetUserShelves(user):
  """Retrive all shelves associated to a user

  Args:
    UserInfo user: UserInfo object representing the user

  Return:
    list: A list of shelves the user has
  """
  err = []
  sysErr = []
  recommenders = []

  try:
      rec = DBAccessConnection.con.execute("SELECT * FROM Recommenders r WHERE r.r_userID = " + str(user.userID) + ";")
      for r in rec:
      	recommender = Recommender(r['recommenderID'], r['r_userID'], r['channelName'], r['timeCreated'])
 	recommenders.append(recommender)
  except:
    sysErr.append("dbGetUserShelves Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (recommenders, None)
  else:
    return (None, (err,sysErr))
  
def dbCreateChannel(user, channelName, seeds):
  """Create a recommendation channel
  
  Args:
    UserInfo user: UserInfo object representing the user
    string channelName: The name of the channel
    seeds: A list of seed wineIDs (all have isSeedBottle = true)

  Return:
    Recommender: A Recommender object representing the new channel
  """
  err = []
  sysErr = []
  time = datetime.datetime.now().replace(microsecond = 0)
  try:
    DBAccessConnection.con.execute(DBAccessConnection.recommenders.insert(), r_userID = user.userID, channelName = channelName, timeCreated = time)
    rec = DBAccessConnection.con.execute("SELECT * FROM Recommenders r WHERE r.r_userID = " + str(user.userID) + " AND r.channelName = " + "\"" + str(channelName) + "\"" + ";").first()
    recommender = Recommender(rec['recommenderID'], rec['r_userID'], rec['channelName'], rec['timeCreated'])
    for wine in seeds:
      DBAccessConnection.con.execute(DBAccessConnection.recommenderHistory.insert(), rh_recommenderID = rec['recommenderID'], rh_wineID = wine, timestamp = time, isSeedBottle = 1)
  except:
    sysErr.append("dbCreateChannel Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (recommender, None)
  else:
    return (None, (err,sysErr))
  

def dbGetRecommender(recommenderID):
  """Get a recommender object.

  Args:
    int recommenderID: ID of the recommender

  Return:
    Recommender: The Recommender object associated with recommenderID
  """
  err = []
  sysErr = []
  
  try:
    rec = DBAccessConnection.con.execute('SELECT * FROM Recommenders rh WHERE rh.recommenderID = ' + str(recommenderID) + ';').first()
    rec = Recommender(rec['recommenderID'], rec['r_userID'], rec['channelName'], rec['timeCreated'])
  except:
    sysErr.append("dbGetRecommender Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (rec, None)
  else:
    return (None, (err,sysErr))
    


def dbEditChannel(recommender, channelName):
  """Edit the name of a channel

  Args:
    Recommender recommender: The recommender
    string channelName: The name to change to

  Return:
    Recommender: The channel whose name was edited.
  """
  DBAccessConnection.con.execute(DBAccessConnection.recommenders.update(DBAccessConnection.recommenders.c.recommenderID==recommender.recommenderID), channelName = channelName)
  recommender.channelName = channelName

  return (recommender, None)

  
def dbRemoveChannel(recommenderID):
  """Remove a recommendation channel
  
  Args:
    int recommenderID: The id of the channel.

  Return:
    Recommender: The channel removed.
  """
  
  err = []
  sysErr = []
  
  try:
    channel = DBAccessConnection.con.execute(DBAccessConnection.recommenders.select(DBAccessConnection.recommenders.c.recommenderID==recommenderID)).first()
  except:
    sysErr.append("recommenderID: " + str(recommenderID) + " not found in database.")
  
  try:
    DBAccessConnection.con.execute(DBAccessConnection.recommenderHistory.delete(DBAccessConnection.recommenderHistory.c.rh_recommenderID==recommenderID))
    DBAccessConnection.con.execute(DBAccessConnection.recommenders.delete(DBAccessConnection.recommenders.c.recommenderID==recommenderID))
  except:
    sysErr.append("dbRemoveChannel(" + str(recommenderID) + ") failed.")
  
  if not err and not sysErr:
    return (channel, (err, sysErr))
  else:
    return (None, (err,sysErr))

def dbSetCSOByWineID(wineID, CSO):
  """ Sets a wine's CSO value to true if CSO == True, false otherwise
      Returns the wine object that it set or an error

  Args:
    int wineID: The ID of the wine
    bool CSO: Boolean value for telling if wine is a cluster supporting object

  Return:
    int: The ID of the wine
  """
  err = []
  sysErr = []

  setCSO = 0

  if CSO == True:
    setCSO = 1

  try:
    DBAccessConnection.con.execute("UPDATE Wines "
              + "SET CSO = " + str(setCSO)
              + " WHERE wineID = " + str(wineID) + ";")
  except:
    sysErr.append("dbSetCSOByWineID failed")
    return (None,(err,sysErr))

  wine = dbGetWineByID(wineID)

  if wine[0] == None:
    sysErr.append("dbSetCSOByWineID failed")
    return (None,(err,sysErr))
  else:
    return (wine[0],(err,sysErr))


def dbSetClusterID(wineID, clusterID):
  """ Sets a wine's cluster ID  to clusterID
      Returns the wine object that it set or an error

  Args:
    int wineID: The ID of the wine
    int clusterID: The cluster ID

  Return:
    int: The ID of the wine
  """
  err = []
  sysErr = []

  #print "wineid: " + str(wineID)
  #print "clusterID: " + str(clusterID)

  try:
    DBAccessConnection.con.execute("UPDATE Wines "
              + "SET clusterID = " + str(clusterID)
              + " WHERE wineID = " + str(wineID) + ";")
  except:
    sysErr.append("dbSetClusterID failed")
    return (None,(err,sysErr))

  wine = dbGetWineByID(wineID)

  if wine[0] == None:
    sysErr.append("dbSetClusterID failed")
    return (None,(err,sysErr))
  else:
    return (wine[0],(err,sysErr))
  
  
def dbAddSeeds(recommenderID, seeds):
  """Add seeds to a channel.
  
  Args:
    int recommenderID: The id of the channel
    list seeds: A list of wineIDs specifying seed DBAccessConnection.wines.

  Return:
    Recommender: The Recommender object just created
  """
  err = []
  sysErr = []
  time = datetime.datetime.now().replace(microsecond = 0)
  try:
    for ids in seeds:
      DBAccessConnection.con.execute(DBAccessConnection.recommenderHistory.insert(), rh_recommenderID = recommenderID, rh_wineID = ids, timestamp = time, isSeedBottle = 1)
    rec = DBAccessConnection.con.execute('SELECT * FROM Recommenders r WHERE r.recommenderID = ' + "\"" + str(recommenderID) + "\"" + ';').first()
    recommender = Recommender(rec['recommenderID'], rec['r_userID'], rec['channelName'], rec['timeCreated'])
  except:
    sysErr.append("dbAddSeeds Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (recommender, None)
  else:
    return (None, (err,sysErr))
  
  
def dbRemoveSeeds(recommenderID, seeds):
  """Remove seeds from a channel.
  
  Args:
    int recommenderID: The id of the channel
    list seeds: A list of wineIDs to remove as seeds.

  Return:
    RecommenderHistory: A blank RecommenderHistory object
  """
  
  err = []
  sysErr = []
  
  for seed in seeds:
    try:
      entry = DBAccessConnection.con.execute('SELECT * FROM RecommenderHistory '
                        + 'WHERE rh_recommenderID = ' + str(recommenderID)
                        + ' AND rh_wineID = ' + str(seed) 
                        + ' AND isSeedBottle = 1;').first()
      if entry == None:
        sysErr.append("dbRemoveSeeds(): seed " + str(seed) + " not found")
    except:
      sysErr.append("dbRemoveSeeds(): seed " + str(seed) + " not found")
      return (None, (err, sysErr))
  
  for seed in seeds:
    try:
      DBAccessConnection.con.execute('DELETE FROM RecommenderHistory '
                + 'WHERE rh_recommenderID = ' + str(recommenderID)
                + ' AND rh_wineID = ' + str(seed) 
                + ' AND isSeedBottle = 1;')
    except:
      sysErr.append("dbRemoveSeeds() failed to remove seed: " + str(seed))
  
  return (RecommenderHistory(), (err, sysErr))
  

def dbShelfWineCandidates (wineDict):
  """Retrieve wines from database with qualities similar to attributes

  Args: 
    dict wineDict: Dictionary of attributes (wineName, winery, vintage)

  Return:
    list: List of wines
  """
  err = []
  sysErr = []
  wineList = []
  if not (wineDict['wineName'] == '' and wineDict['winery'] == '' and wineDict['vintage'] == ''):
    try:
      query = 'SELECT * FROM Wines WHERE '

      terms = list()
      if len(wineDict['wineName']) > 0:
        terms.append('wineName LIKE \'%%' + wineDict['wineName'] + '%%\'')
      if len(wineDict['winery']) > 0:
        terms.append('winery LIKE \'%%' + wineDict['winery'] + '%%\'')
      if len(wineDict['vintage']) > 0:
        terms.append('vintage LIKE \'%%' + wineDict['vintage'] + '%%\'')

      for i in range(0, len(terms)):
        if i != 0:
          query = query + ' AND '
        query = query + terms[i]
      query = query + ';'

      candWines = DBAccessConnection.con.execute(query)
      for wine in candWines:
        candidate = Wine(wine['wineID'],wine['wineName'],wine['varietal'],wine['winery'],wine['wineType'],wine['vintage'],wine['region'],wine['clusterID'],wine['CSO'],wine['tags'],wine['description'],wine['averageStarRating'],wine['imagePath'],wine['barcode'],wine['bitter'],wine['sweet'],wine['sour'],wine['salty'],wine['chemical'],wine['pungent'],wine['oxidized'],wine['microbiological'],wine['floral'],wine['spicy'],wine['fruity'],wine['vegetative'],wine['nutty'],wine['caramelized'],wine['woody'],wine['earthy'])
        wineList.append(candidate)
    except:
      sysErr.append("dbShelfWineCandidates Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (wineList, None)
  else:
    return (None, (err,sysErr))

def dbGetRecommenderHistory(channelID):
  """Retrieve list of wines previously recommended

  Args: 
    int channelID: ID of the channel whose recommender history we want to get

  Return: 
    list: A list of RecommenderHistory objects
  """
  err = []
  sysErr = []
  recommendedList = []
  try:
    recHist = DBAccessConnection.con.execute('SELECT * FROM RecommenderHistory rh WHERE rh.rh_recommenderID = ' + str(channelID) + ';')
    for recRow in recHist:
      hist = RecommenderHistory(recRow['rh_index'], recRow['rh_recommenderID'], recRow['rh_wineID'], recRow['timestamp'], recRow['isSeedBottle'])
      recommendedList.append(hist)
  except:
    sysErr.append("dbGetRecommenderHistory Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (recommendedList, None)
  else:
    return (None, (err,sysErr))


def dbGetWinesByName(name):
  """Retrieve wines from database with the given name

  Args:
    string name: The name of the wine

  Return:
    Wine: The list of wines with the name specified
  """
  err = []
  sysErr = []
  wines = []
  try:
    wine = DBAccessConnection.wines.select(DBAccessConnection.wines.c.wineName == name).execute().first()
    wine2 = Wine(wine['wineID'],wine['wineName'],wine['varietal'],wine['winery'],wine['wineType'],wine['vintage'],wine['region'],wine['clusterID'],wine['CSO'],wine['tags'],wine['description'],wine['averageStarRating'],wine['imagePath'],wine['barcode'],wine['bitter'],wine['sweet'],wine['sour'],wine['salty'],wine['chemical'],wine['pungent'],wine['oxidized'],wine['microbiological'],wine['floral'],wine['spicy'],wine['fruity'],wine['vegetative'],wine['nutty'],wine['caramelized'],wine['woody'],wine['earthy'])
    wines.append(wine2)
  except:
    sysErr.append("dbGetWinesByName Error found")
  if (len(err) == 0 and len(sysErr) == 0):
  	return (wines, None)
  else:
  	return (None, (err, sysErr))

def dbAddWineGlobal(wine):
  """Add a new wine to the global database

  Args:
    Wines wine: The wine to be inserted into the database

  Return:
    Wine: The wine just added to the database
  """

  err = []
  sysErr = []

  try:
    DBAccessConnection.con.execute(DBAccessConnection.wines.insert(), wineName = wine.wineName, varietal = wine.varietal, winery = wine.winery, wineType = wine.wineType, vintage = wine.vintage, region = wine.region, clusterID = wine.clusterID, CSO = wine.CSO, tags = wine.tags, description = wine.description, averageStarRating = wine.averageStarRating, imagePath = wine.imagePath, barcode = wine.barcode, bitter = wine.bitter, sweet = wine.sweet, sour = wine.sour, salty = wine.salty, chemical = wine.chemical, pungent = wine.pungent, oxidized = wine.oxidized, microbiological = wine.microbiological, floral = wine.floral, spicy = wine.spicy, fruity = wine.fruity, vegetative = wine.vegetative, nutty = wine.nutty, caramelized = wine.caramelized, woody = wine.woody, earthy = wine.earthy)
    wine2 = DBAccessConnection.con.execute('SELECT * FROM Wines w WHERE w.wineName = ' + "\"" + str(wine.wineName) + "\"" + ' AND w.winery = ' + "\"" + str(wine.winery) + "\"" + ' AND w.vintage = ' + str(wine.vintage) +';').first()
    wine.wineID = wine2['wineID']
  except:
    sysErr.append("Error found in dbAddWineGlobal")
  if (len(err) == 0 and len(sysErr) == 0):
    return (wine, None)
  else:
    return (None, (err, sysErr))

def dbGetWineGlobal(wineID):
  """ Retrieves a wine from the global database based on it's wineID

  Args:
    int wineID: The ID of the wine

  Return:
    Wine: The wine with ID wineID
  """
  
  err = []
  sysErr = []
  
  try:
    wine = DBAccessConnection.wines.select(DBAccessConnection.wines.c.wineID==wineID).execute().first()
    wine2 = Wine(wineID = wine['wineID'], wineName = wine['wineName'], varietal = wine['varietal'], winery = wine['winery'], wineType = wine['wineType'], vintage = wine['vintage'], region = wine['region'], clusterID = wine['clusterID'], CSO = wine['CSO'], tags = wine['tags'], description = wine['description'], averageStarRating = wine['averageStarRating'], imagePath = wine['imagePath'], barcode = wine['barcode'], bitter = wine['bitter'], sweet = wine['sweet'], sour = wine['sour'], salty = wine['salty'], chemical = wine['chemical'], pungent = wine['pungent'], oxidized = wine['oxidized'], microbiological = wine['microbiological'], floral = wine['floral'], spicy = wine['spicy'], fruity = wine['fruity'], vegetative = wine['vegetative'], nutty = wine['nutty'], caramelized = wine['caramelized'], woody = wine['woody'], earthy = wine['earthy'])
  except:
    sysErr.append("Get wine from global database failed.")
  if (len(err) == 0 and len(sysErr) == 0):
    return (wine2, None)
  else:
    return (None, (err, sysErr))
  
def dbDeleteWineGlobal(wine):
  """Delete wine from the global database

  Args:
    Wines wine: The wine to be removed from the database

  Return:
    Wine: The wine just removed
  """
  err = []
  sysErr = []

 	#delete any entries of this wine in LocationInventory, LocationHistory, and RecommenderHistory tables
  DBAccessConnection.con.execute(DBAccessConnection.locationInventory.delete(DBAccessConnection.locationInventory.c.li_wineID==wine.wineID))
  DBAccessConnection.con.execute(DBAccessConnection.locationHistory.delete(DBAccessConnection.locationHistory.c.lh_wineID==wine.wineID))
  DBAccessConnection.con.execute(DBAccessConnection.recommenderHistory.delete(DBAccessConnection.recommenderHistory.c.rh_wineID==wine.wineID))
  DBAccessConnection.con.execute(DBAccessConnection.wines.delete(DBAccessConnection.wines.c.wineID==wine.wineID))
  
  return (wine, (err, sysErr))

def dbRateWineGlobal(wine, rating):
  """Update the global rating of a wine in database

  Args:
    Wines wine: The wine whose rating will be updated
    int rating: The rating of the wine being added

  Return:
    Wine: The wine whose rating was updated
  """
  
  err = []
  sysErr = []
  
  DBAccessConnection.con.execute("UPDATE Wines w "
            + "SET w.averageStarRating = ( "
            + "SELECT avg( li.personalStarRating ) "
            + "FROM LocationInventory li "
            + "WHERE li.li_wineID = " + str(wine.wineID) 
            + " ) "
            + "WHERE w.wineID = " + str(wine.wineID) + ";")
  
  return (wine, (err, sysErr))
  
def dbGetWineIDs():
  """Retrieve all wineIDs from the Wines table. For use in dbRandomWine

  Args:
    None

  Return:
    list: List containing all wineIDs in the Wines table

  """
  err = []
  sysErr = []
  wineIDlist = []
  try:
    wineIDs = DBAccessConnection.con.execute("SELECT w.wineID FROM Wines w;")
  except:
    sysErr.append("dbGetWineIDs Error found")

  for w in wineIDs:
      wineIDlist.append(w['wineID'])

  if (len(err) == 0 and len(sysErr) == 0):
    return (wineIDlist, None)
  else:
    return (None, (err,sysErr))
  
def dbRandomWine():
  """Retrieve a random wine from database

  Args:
    None

  Return:
    Wine: A random wine from the Wines table
  """
  err = []
  sysErr = []
  try:
    idList = dbGetWineIDs()[0]
  except:
    sysErr['syserror'] = "Error getting wines"
  randomID = random.randrange(1, len(idList))
  try:
    rwine = DBAccessConnection.con.execute('SELECT * FROM Wines w WHERE w.wineID = ' + str(randomID) + ';')
    for wine in rwine:
      randwine = Wine(wine['wineID'],wine['wineName'],wine['varietal'],wine['winery'],wine['wineType'],wine['vintage'],wine['region'],wine['clusterID'],wine['CSO'],wine['tags'],wine['description'],wine['averageStarRating'],wine['imagePath'],wine['barcode'],wine['bitter'],wine['sweet'],wine['sour'],wine['salty'],wine['chemical'],wine['pungent'],wine['oxidized'],wine['microbiological'],wine['floral'],wine['spicy'],wine['fruity'],wine['vegetative'],wine['nutty'],wine['caramelized'],wine['woody'],wine['earthy'])
  except:
    sysErr.append("dbRandomWine Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (randwine, None)
  else:
    return (None, (err,sysErr))
  
def dbGetCSOs():
  """"Retrieve all CSOs 
  
  Return a list of all CSOs

  Args:
    None
  
  Return:
    list: A list of all CSO Wine objects
  """
  err = []
  sysErr = []
  try:
    csoList = []
    clusterObjects = DBAccessConnection.wines.select(DBAccessConnection.wines.c.CSO == 1).execute()
    for wine in clusterObjects:
      csoList.append(Wine(wine['wineID'],wine['wineName'],wine['varietal'],wine['winery'],wine['wineType'],wine['vintage'],wine['region'],wine['clusterID'],wine['CSO'],wine['tags'],wine['description'],wine['averageStarRating'],wine['imagePath'],wine['barcode'],wine['bitter'],wine['sweet'],wine['sour'],wine['salty'],wine['chemical'],wine['pungent'],wine['oxidized'],wine['microbiological'],wine['floral'],wine['spicy'],wine['fruity'],wine['vegetative'],wine['nutty'],wine['caramelized'],wine['woody'],wine['earthy']))
  except:
    sysErr.append("dbGetCSOs Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (csoList, None)
  else:
    return (None, (err,sysErr))
  
  
def dbGetWinesInCluster(w):
  """"Retrieve all wines in the cluster described by the cso
  
  Return a list of all wines in the cluster defined by cso.
  
  Args:
    Wine w: The wine representing the CSO to grab wines from
    
  Return:
    list: A list of all wines belonging to the cluster.
  """

  err = []
  sysErr = []
  csolist = []
  try:
    csowines = DBAccessConnection.wines.select(DBAccessConnection.wines.c.clusterID == w.clusterID).execute()
    for wine in csowines:
      csolist.append(Wine(wine['wineID'],wine['wineName'],wine['varietal'],wine['winery'],wine['wineType'],wine['vintage'],wine['region'],wine['clusterID'],wine['CSO'],wine['tags'],wine['description'],wine['averageStarRating'],wine['imagePath'],wine['barcode'],wine['bitter'],wine['sweet'],wine['sour'],wine['salty'],wine['chemical'],wine['pungent'],wine['oxidized'],wine['microbiological'],wine['floral'],wine['spicy'],wine['fruity'],wine['vegetative'],wine['nutty'],wine['caramelized'],wine['woody'],wine['earthy']))
  except:
    sysErr.append("dbGetWinesInCluster Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (csolist, None)
  else:
    return (None, (err,sysErr))

def dbGetFeatureVector():
  """Retrieve the reference wine (wine ID = 0)
  
  Args:
    None

  Return:
    Wine: The wine with wineID = 0
  """

  err = []
  sysErr = []
  try:
    referenceWine = DBAccessConnection.con.execute('SELECT * FROM Wines w WHERE w.wineID = 0;').first()
  except:
    sysErr.append("dbGetFeatureVector Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (dict(referenceWine), None)
  else:
    return (None, (err, sysErr))

def dbGetSeeds(channelID):
  """"Retrieve all seed wines for a particular channel

  Args:
    int channelID: ID of channel
  
  Return: 
    list: List of seed wines
  """
  err = []
  sysErr = []
  seedList = []
  try:
    # This returns row proxies of recommender history objects
    seeds = DBAccessConnection.con.execute('SELECT * FROM RecommenderHistory rh WHERE rh.rh_recommenderID = ' + str(channelID) + ' AND rh.isSeedBottle = 1;')
    for wine in seeds:
      seed = dbGetWineGlobal(wine['rh_wineID'])
      if seed[0] == None:
        sysErr.append("Error getting global wine")
        return (None, (err,sysErr))
      else:
        seed = seed[0]
      seedList.append(seed)
  except:
    sysErr.append("dbGetSeeds Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (seedList, None)
  else:
    return (None, (err,sysErr))


def dbAddRecommenderHistory(rh):
  """ Adds a recommendation history object to the channel specified

  Args:
    RecommenderHistory rh: The RecommenderHistory object to be added

  Return:
    RecommenderHistory: The RecommenderHistory object just added
  """

  err = []
  sysErr = []
  time = datetime.datetime.now().replace(microsecond = 0)
  try:
    DBAccessConnection.con.execute(DBAccessConnection.recommenderHistory.insert(), rh_recommenderID = rh.rh_recommenderID, rh_wineID = rh.rh_wineID, timestamp = time, isSeedBottle = rh.isSeedBottle)
  except:
    sysErr.append("dbAddRecommender history failed")
    return (None, (err,sysErr))

  return(rh, None)