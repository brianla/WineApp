""" Methods to access the database in relation to inventory tasks """

from flask import *
from Classes import *
from InstantiationValidation import *
import Globals
from sqlalchemy import *
import random
import sys
import datetime
import DBAccessConnection


DEBUG = False

def dbGetInventory(user):
  """Retrieve a user's inventory from database
  Return a list of LocationInventory objects representing the wines in a user's inventory.

  Args:
    UserInfo user: The user whose inventory will be retrieved

  Return:
    list: A list of LocationInventory objects detailing the user's entire inventory.
  """
  locations = DBAccessConnection.con.execute('SELECT * FROM LocationMap lm WHERE lm.lm_userID = ' + str(user.userID) + ';')

  err = []
  sysErr = []
  inventoryList = []
  try:
    for row in locations:
      locationInventories = DBAccessConnection.con.execute('SELECT * FROM LocationInventory li WHERE li.li_locationID = ' + str(row['locationID']) + ';')
      for locInv in locationInventories:
        inv = LocationInventory(locInv['li_index'], locInv['li_locationID'], locInv['li_wineID'], locInv['quantity'], locInv['tags'], locInv['description'], locInv['imagePath'], locInv['personalStarRating'], locInv['isWishlist'], locInv['bitter'], locInv['sweet'], locInv['sour'], locInv['salty'], locInv['chemical'], locInv['pungent'], locInv['oxidized'], locInv['microbiological'], locInv['floral'], locInv['spicy'], locInv['fruity'], locInv['vegetative'], locInv['nutty'], locInv['caramelized'], locInv['woody'], locInv['earthy'])
        inventoryList.append(inv)
  except:
    sysErr.append("dbGetInventory Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (inventoryList, None)
  else:
    return (None, (err,sysErr))

def dbGetWideInventory(user):
  """Retrieve all wines from all inventories associated to a user

  Args:
    UserInfo user: The user whose wines will be returned

  Return:
    list: A list of all wines associated to a user
  """
  err = []
  sysErr = []
  dictList = []
  try:
    results = DBAccessConnection.con.execute(' SELECT w.wineID as wine_wineID, w.wineName as wine_wineName, w.varietal as wine_varietal, w.winery as wine_winery, w.wineType as wine_wineType, w.vintage as wine_vintage, w.region as wine_region, w.clusterID as wine_clusterID, w.CSO as wine_CSO, w.tags as wine_tags, w.description as wine_description, w.averageStarRating as wine_averageStarRating, w.imagePath as wine_imagePath, w.barcode as wine_barcode, w.bitter as wine_bitter, w.sweet as wine_sweet, w.sour as wine_sour, w.salty as wine_salty, w.chemical as wine_chemical, w.pungent as wine_pungent, w.oxidized as wine_oxidized, w.microbiological as wine_microbiological, w.floral as wine_floral, w.spicy as wine_spicy, w.fruity as wine_fruity, w.vegetative as wine_vegetative, w.nutty as wine_nutty, w.caramelized as wine_caramelized, w.woody as wine_woody, w.earthy as wine_earthy, li.li_index as user_li_index, li.li_locationID as user_li_locationID, li.li_wineID as user_li_wineID, li.quantity as user_quantity, li.tags as user_tags, li.description as user_description, li.imagePath as user_imagePath, li.personalStarRating as user_personalStarRating, li.isWishlist as user_isWishlist, li.bitter as user_bitter, li.sweet as user_sweet, li.sour as user_sour, li.salty as user_salty, li.chemical as user_chemical, li.pungent as user_pungent, li.oxidized as user_oxidized, li.microbiological as user_microbiological, li.floral as user_floral, li.spicy as user_spicy, li.fruity as user_fruity, li.vegetative as user_vegetative, li.nutty as user_nutty, li.caramelized as user_caramelized, li.woody as user_woody, li.earthy as user_earthy ' +
                          ' FROM Wines w, LocationInventory li ' +
                          ' WHERE w.wineID = li.li_wineID ' +
                          ' AND li.li_locationID IN ( ' +
                          ' SELECT lm.locationID ' +
                          ' FROM LocationMap lm ' +
                          ' WHERE lm.lm_userID = ' + str(user.userID) + ') ORDER BY w.wineID DESC;')
    usedWineIDs = set()
    for proxy in results:
      if str(proxy['wine_wineID']) not in usedWineIDs:
       
        #Make Dictionary, add to list

        dictList.append(dict(proxy))

        #Add wineID to used list
        usedWineIDs.add(str(proxy['wine_wineID']))
  except KeyError:
    sysErr.append('Key Error when accessing wineID in Proxy')
  except:
    sysErr.append('Crzy SQL Query Failed')
  if (len(err) == 0 and len(sysErr) == 0):
    return (dictList, None)
  else:
    return (None, (err,sysErr))

def dbGetWideInventoryByDate(user):
  """Retrieve all wines from all inventories associated to a user sorted by timestamp

  Args:
    UserInfo user: The user whose wines will be returned

  Return:
    list: A list of all wines associated to a user sorted by timestamp
  """
  err = []
  sysErr = []
  dictList = []
  try:
    results = DBAccessConnection.con.execute(' SELECT w.wineID as wine_wineID, w.wineName as wine_wineName, w.varietal as wine_varietal, w.winery as wine_winery, w.wineType as wine_wineType, w.vintage as wine_vintage, w.region as wine_region, w.clusterID as wine_clusterID, w.CSO as wine_CSO, w.tags as wine_tags, w.description as wine_description, w.averageStarRating as wine_averageStarRating, w.imagePath as wine_imagePath, w.barcode as wine_barcode, w.bitter as wine_bitter, w.sweet as wine_sweet, w.sour as wine_sour, w.salty as wine_salty, w.chemical as wine_chemical, w.pungent as wine_pungent, w.oxidized as wine_oxidized, w.microbiological as wine_microbiological, w.floral as wine_floral, w.spicy as wine_spicy, w.fruity as wine_fruity, w.vegetative as wine_vegetative, w.nutty as wine_nutty, w.caramelized as wine_caramelized, w.woody as wine_woody, w.earthy as wine_earthy, li.li_index as user_li_index, li.li_locationID as user_li_locationID, li.li_wineID as user_li_wineID, li.quantity as user_quantity, li.tags as user_tags, li.description as user_description, li.imagePath as user_imagePath, li.personalStarRating as user_personalStarRating, li.isWishlist as user_isWishlist, li.bitter as user_bitter, li.sweet as user_sweet, li.sour as user_sour, li.salty as user_salty, li.chemical as user_chemical, li.pungent as user_pungent, li.oxidized as user_oxidized, li.microbiological as user_microbiological, li.floral as user_floral, li.spicy as user_spicy, li.fruity as user_fruity, li.vegetative as user_vegetative, li.nutty as user_nutty, li.caramelized as user_caramelized, li.woody as user_woody, li.earthy as user_earthy ' +
                          ' FROM Wines w, LocationInventory li ' +
                          ' WHERE w.wineID = li.li_wineID ' +
                          ' AND li.li_locationID IN ( ' +
                          ' SELECT lm.locationID ' +
                          ' FROM LocationMap lm ' +
                          ' WHERE lm.lm_userID = ' + str(user.userID) + ');')
    usedWineIDs = set()
    for proxy in results:
      if str(proxy['wine_wineID']) not in usedWineIDs:

        #Make Dictionary, add to list

        dictList.append(dict(proxy))

        #Add wineID to used list
        usedWineIDs.add(str(proxy['wine_wineID']))
  except KeyError:
    sysErr.append('Key Error when accessing wineID in Proxy')
  except:
    sysErr.append('Crzy SQL Query Failed')
  #Sort dictList by timestamp
  dictList.sort(key = lambda dlist: dlist['timestamp'], reverse = True)
  if (len(err) == 0 and len(sysErr) == 0):
    return (dictList, None)
  else:
    return (None, (err,sysErr))

def dbGetHistoryByLocation(locMap):
  """Return all wine history from a particular location
    
  Args: 
    LocationMap locMap: A location map object

  Return: 
    list: A list of LocationHistory objects
  """
  err = []
  sysErr = []
  locHist = []
  try:
    location = DBAccessConnection.locationHistory.select(DBAccessConnection.locationHistory.c.lh_locationID == locMap.locationID).execute()
    for row in location:
      locHist.append(LocationHistory(row['lh_index'],row['lh_locationID'],row['lh_wineID'],row['timestamp'],row['eventTag']))
  except:
    sysErr.append("dbGetHistoryByLocation Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (locHist, None)
  else:
    return (None, (err,sysErr))

def dbGetInventoryMap(user):
  """ Returns the user's inventory MAP
     Very helpful for making the XML =)
     BTW: What I am thinking is that said map will
     tell me what all the wines are for a particular
     location. As I interpret the db diagram, that's what
     the InventoryMap is.
     I am assuming the key is the locationID

  Args: 
    UserInfo user: User whose InventoryMap will be retrieved

  Return:
    list: A list of all inventories associated to a user
  """
  err = []
  sysErr = []
  inventories = []
  try:
    inventory = DBAccessConnection.locationMap.select(DBAccessConnection.locationMap.c.lm_userID == user.userID).execute()
    for rows in inventory:
      inventories.append(locationMap(row['locationID'],row['lm_userID'],row['locationName'],row['timeCreated'],row['imagePath']))
  except:
    sysErr.append("dbGetInventoryMap Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (inventories, None)
  else:
    return (None, (err,sysErr))
  
def dbGetUserLocations(userID):
  """Retrieve a list of locations associated to a user

  Args: 
    UserInfo userID: ID of user

  Returns: 
    list: A list of LocationMap objects
  """
  err = []
  sysErr = []
  locList = []
  try:
    locs = DBAccessConnection.con.execute('SELECT * FROM LocationMap lm WHERE lm.lm_userID = ' + str(userID) + ';')
    for loc in locs:
      locID = int(loc['locationID'])
      location = dbGetLocation(locID)
      locList.append(location[0])
  except:
    sysErr.append("dbGetuserLocations Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (locList, None)
  else:
    return (None, (err, sysErr))

  
def dbGetLocation(locID):
  """Retrieve a user's inventory location
  Retrieve an inventory location from the location map.
  
  Args:
   int locID: The locationID of the location.
  
  Return:
   LocationMap: The LocationMap object of the location.
  """

  err = []
  sysErr = []
  try:
    locMap = DBAccessConnection.con.execute('SELECT * FROM LocationMap lm WHERE lm.locationID = ' + str(locID) + ';').first()
    locs = LocationMap(locMap['locationID'], locMap['lm_userID'], locMap['locationName'], locMap['timeCreated'], locMap['imagePath'])
  except:
    sysErr.append("dbGetLocation Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (locs, None)
  else:
    return (None, (err, sysErr))

def dbGetAllWines():
  """Retrieve all wines in the database

  Args:
    None

  Return: 
    list: The list of all wines
  """
  err = []
  sysErr = []
  wineList = []
  try:
    wines = DBAccessConnection.con.execute('SELECT * FROM Wines;')
    for wine in wines:
      wine1 = Wine(wine['wineID'],wine['wineName'],wine['varietal'],wine['winery'],wine['wineType'],wine['vintage'],wine['region'],wine['clusterID'],wine['CSO'],wine['tags'],wine['description'],wine['averageStarRating'],wine['imagePath'],wine['barcode'],wine['bitter'],wine['sweet'],wine['sour'],wine['salty'],wine['chemical'],wine['pungent'],wine['oxidized'],wine['microbiological'],wine['floral'],wine['spicy'],wine['fruity'],wine['vegetative'],wine['nutty'],wine['caramelized'],wine['woody'],wine['earthy'])
      wineList.append(wine1)
  except:
    sysErr.append("Found error in dbGetAllWines")
  if (len(err) == 0 and len(sysErr) == 0):
    return (wineList, None)
  else:
    return (None, (err, sysErr))
    
def dbGetWineByID (wineID):
  """Retrieve a wine by its ID

  Args:
    int wineID: The wineID of the wine

  Return:
    Wine: The Wine object with the specified ID
  """
  err = []
  sysErr = []
  try:
    wine = DBAccessConnection.con.execute('SELECT * FROM Wines w WHERE w.wineID = ' + str(wineID) + ';').first()
    wine1 = Wine(wine['wineID'],wine['wineName'],wine['varietal'],wine['winery'],wine['wineType'],wine['vintage'],wine['region'],wine['clusterID'],wine['CSO'],wine['tags'],wine['description'],wine['averageStarRating'],wine['imagePath'],wine['barcode'],wine['bitter'],wine['sweet'],wine['sour'],wine['salty'],wine['chemical'],wine['pungent'],wine['oxidized'],wine['microbiological'],wine['floral'],wine['spicy'],wine['fruity'],wine['vegetative'],wine['nutty'],wine['caramelized'],wine['woody'],wine['earthy'])
  except:
    sysErr.append("dbGetWineByID Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (wine1, None)
  else:
    return (None, (err, sysErr))

def dbGetWineUser(wineID, locationID):
  """Retrieve a user's wine from inventory
  Retrieve the specified wine from the user's location.

  Args:
   int wineID: The wineID of the wine.
   int locationID: The locationID of the wine's location.
  
  Return:
   LocationInventory: The LocationInventory object of the wine.
  """
  err = []
  sysErr = []

  try:
    loc = DBAccessConnection.con.execute("SELECT * FROM LocationInventory li WHERE li.li_wineID = " + str(wineID) + " AND li.li_locationID = " + str(locationID) +";").first()
    locInv = LocationInventory(loc['li_index'], loc['li_locationID'], loc['li_wineID'], loc['quantity'], loc['tags'], loc['description'], loc['imagePath'], loc['personalStarRating'], loc['isWishlist'], loc['bitter'], loc['sweet'], loc['sour'], loc['salty'], loc['chemical'], loc['pungent'], loc['oxidized'], loc['microbiological'], loc['floral'], loc['spicy'], loc['fruity'], loc['vegetative'], loc['nutty'], loc['caramelized'], loc['woody'], loc['earthy'])
  except:
    sysErr.append("dbGetWineUser Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (locInv, (err, sysErr))
  else:
    return (None, (err, sysErr))
  
def dbAddWineUser(wine, count,user):
  """Add a wine to the user's inventory in database
  Insert the given wine into the specified inventory.
  Include the attributes in wine, which will include a new
  wineID.

  Args:
   LocationInventory wine: A LocationInventory object representing a wine.
   int count: The number of this wine to add.

  Return:
    Wine: The wine just added
  """
  err = []
  sysErr = []
  try:
    DBAccessConnection.con.execute(DBAccessConnection.locationInventory.insert(), li_locationID = wine.li_locationID, li_wineID = wine.li_wineID, quantity = wine.quantity, tags = wine.tags, description = wine.description, imagePath = wine.imagePath, personalStarRating = wine.personalStarRating, isWishlist = wine.isWishlist, bitter = wine.bitter, sweet = wine.sweet, sour = wine.sour, salty = wine.salty, chemical = wine.chemical, pungent = wine.pungent, oxidized = wine.oxidized, microbiological = wine.microbiological, floral = wine.floral, spicy = wine.spicy, fruity = wine.fruity, vegetative = wine.vegetative, nutty = wine.nutty, caramelized = wine.caramelized, woody = wine.woody, earthy = wine.earthy)
  except:
    sysErr.append("dbAddWineUser Error found")
  if (len(err) == 0 and len(sysErr) == 0):
    return (wine, None)
  else:
    return (None, (err,sysErr))

def dbUpdateWineCount(locationID, wineID, addCount):
  """ Adds addCount to the quantity of the LocationInventory wine entry specified
      by locationID and wineID.

  Args:
    int locationID: The ID of the location where the wine count will be updated
    int wineID: The ID of the wine to be updated
    int addCount: The number of wines that will be added/removed

  Return:
    LocationInventory: The LocationInventory object whose count was updated
  """
  
  err = []
  sysErr = []
  
  try:
    count = DBAccessConnection.con.execute("SELECT li.quantity "
                      + "FROM LocationInventory li "
                      + "WHERE li.li_locationID = " + str(locationID)
                      + " AND li.li_wineID = " + str(wineID) + ";").first()['quantity']
    DBAccessConnection.con.execute("UPDATE LocationInventory "
              + "SET quantity = " + str(count + addCount)
              + " WHERE li_locationID = " + str(locationID)
              + " AND li_wineID = " + str(wineID) + ";")
  except:
    sysErr.append("Updating wine quantity failed.")
    return (None, (err, sysErr))
  
  return dbGetWineUser(locationID, wineID)

def dbAddInventory(location):
  """Add a new inventory location to user's profile in database
  Insert a new inventory location into the user's Location Map.

  Args:
    LocationMap location: The LocationMap object of the location.

  Return:
    LocationMap: The LocationMap object added to the database.
  """
  err = []
  sysErr = []
  location1 = DBAccessConnection.con.execute("SELECT * FROM LocationMap lm WHERE lm.lm_userID = " + str(location.lm_userID) + " AND lm.locationName = " + "\"" +  str(location.locationName) + "\"" + ";").first()
  try:
    temp = location1['locationName']
    sysErr.append("Entry already exists")
    return (None, (err, sysErr))
  except:
    try:
      DBAccessConnection.con.execute(DBAccessConnection.locationMap.insert(), lm_userID = location.lm_userID, locationName = location.locationName, timeCreated = location.timeCreated, imagePath = location.imagePath)
    except:
      sysErr.append("dbAddInventory Error found")
    if (len(err) == 0 and len(sysErr) == 0):
      return (location,(err,sysErr)) 
    else:
      return (None, (err,sysErr))
      		
def dbAddLocationHistory(history):
  """Add a new location history to the database.
  Insert a new location history into the database.

  Args:
   LocationHistory: The LocationHistory object representing the new history.
  """
  err = []
  sysErr = []
  try: 
   	DBAccessConnection.con.execute(DBAccessConnection.locationHistory.insert(), lh_locationID = history.lh_locationID, lh_wineID = history.lh_wineID, timestamp = history.timestamp, eventTag = history.eventTag)
  except:
   	sysErr.append("dbAddLocationHistory Error found")
  if (len(err) == 0 and len(sysErr) == 0):
   	return (history, None)
  else:
   	return (None, (err,sysErr))
  
def dbDeleteWineUser(wine):
  """Delete a wine from user's inventory in database
  Delete count amounts of the wine from the user's locations.

  Args:
    LocationInventory wine: The LocationInventory object of the wine.

  Return:
    Wine: The wine just deleted from the user's inventory.
  """
  
  err = []
  sysErr = []
  
  try:
    DBAccessConnection.con.execute('DELETE FROM LocationInventory '
              + 'WHERE li_locationID = ' + str(wine.li_locationID)
              + ' AND li_wineID = ' + str(wine.li_wineID) + ';')
  except:
    sysErr.append("Failed to remove wine from user location inventory.")
    return (None,(err, sysErr))
  
  return (wine, (err, sysErr))
  
  
def dbDeleteInventory(location):
  """Delete a user's inventory location in database
  Delete an inventory location from user's Location Map.

  Args:
   LocationInventory: The LocationInventory object of the location just deleted from the database.
  """
  
  err = []
  sysErr = []
  
  DBAccessConnection.con.execute(DBAccessConnection.locationInventory.delete(DBAccessConnection.locationInventory.c.li_locationID==location.locationID))
  DBAccessConnection.con.execute(DBAccessConnection.locationHistory.delete(DBAccessConnection.locationHistory.c.lh_locationID==location.locationID))
  DBAccessConnection.con.execute(DBAccessConnection.locationMap.delete(DBAccessConnection.locationMap.c.locationID==location.locationID))
  
  return (location, (err, sysErr))
  

def dbEditInventory(location):
  """Edit a user's inventory
  Edit the properties of an inventory location. For every property specified in
  changes, replace the corresponding old property with the new one.

  Args:
    LocationMap location: The LocationMap object of the location being modified. All
                          changes have already been applied.

  Return:
    LocationMap: The location being modified.
  """
  
  err = []
  sysErr = []

  loc = DBAccessConnection.con.execute("SELECT * FROM LocationMap lm WHERE lm.locationName = " + "\"" + str(location.locationName) + "\"" + " AND lm.lm_userID = " + str(location.lm_userID) + ";").first()

  if loc is not None:
    err.append("Location with inputted name already exists")
    return (None, (err,sysErr))
  
  DBAccessConnection.con.execute(DBAccessConnection.locationMap.update(DBAccessConnection.locationMap.c.locationID==location.locationID),
              lm_userID = location.lm_userID, locationName = location.locationName,
              timeCreated = location.timeCreated, imagePath = location.imagePath)
  
  return (location, (err, sysErr))
  

def dbEditEntryUser(wine, oldli):
  """Edit a wine in the user's inventory
  Edit the properties of a wine. For every property specified in
  changes, replace the corresponding old property with the new one.

  Args:
    LocationInventory wine: The LocationInventory object of the wine to be edited. All
                           changes have already been applied.

  Return:
    LocationInventory: The wine that was edited.
  """
  err = []
  sysErr = []
 
  try:
    DBAccessConnection.con.execute(DBAccessConnection.locationInventory.update(and_(DBAccessConnection.locationInventory.c.li_locationID==oldli, DBAccessConnection.locationInventory.c.li_wineID==wine.li_wineID)), 
                li_locationID = wine.li_locationID, li_wineID = wine.li_wineID, 
                quantity = wine.quantity, tags = wine.tags, description = wine.description, 
                imagePath = wine.imagePath, personalStarRating = wine.personalStarRating, 
                isWishlist = wine.isWishlist, bitter = wine.bitter, sweet = wine.sweet, 
                sour = wine.sour, salty = wine.salty, chemical = wine.chemical, 
                pungent = wine.pungent, oxidized = wine.oxidized, 
                microbiological = wine.microbiological, floral = wine.floral, 
                spicy = wine.spicy, fruity = wine.fruity, vegetative = wine.vegetative, 
                nutty = wine.nutty, caramelized = wine.caramelized, woody = wine.woody, 
                earthy = wine.earthy)
  except:
    err.append("Wine edit in location inventory failed")
  
  return (wine, (err, sysErr))

def dbEditWineGlobal(wine):
  """Edit a wine in the global database

  Args:
    Wines wine: The wine that will be edited

  Return:
    Wine: The wine that was edited.
  """

  err = []
  sysErr = []

  try:
    DBAccessConnection.con.execute(DBAccessConnection.wines.update(DBAccessConnection.wines.c.wineID==wine.wineID), wineName = wine.wineName, varietal = wine.varietal, winery = wine.winery, wineType = wine.wineType, vintage = wine.vintage, region = wine.region, clusterID = wine.clusterID, CSO = wine.CSO, tags = wine.tags, description = wine.description, averageStarRating = wine.averageStarRating, imagePath = wine.imagePath, barcode = wine.barcode, bitter = wine.bitter, sweet = wine.sweet, sour = wine.sour, salty = wine.salty, chemical = wine.chemical, pungent = wine.pungent, oxidized = wine.oxidized, microbiological = wine.microbiological, floral = wine.floral, spicy = wine.spicy, fruity = wine.fruity, vegetative = wine.vegetative, nutty = wine.nutty, caramelized = wine.caramelized, woody = wine.woody, earthy = wine.earthy)
    wine2 = DBAccessConnection.con.execute('SELECT * FROM Wines w WHERE w.wineName = ' + "\"" + str(wine.wineName) + "\"" + ' AND w.winery = ' + "\"" + str(wine.winery) + "\"" + ' AND w.vintage = ' + str(wine.vintage) +';').first()
    wine.wineID = wine2['wineID']
  except:
    sysErr.append("Error found in dbAddWineGlobal")
  if (len(err) == 0 and len(sysErr) == 0):
    return (wine, None)
  else:
    return (None, (err, sysErr))

