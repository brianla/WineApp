"""Inventory system processing module
"""
from datetime import datetime
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
#from flask import *
from Classes import *
from InstantiationValidation import *
from UserModelAccess import *
from InventoryModelAccess import *
from RecommenderModelAccess import *
import Globals

DEBUG = True


############# Get Methods #######################


def getWine(locationID, wineID):
  """Retrieve wine from user's inventory
  
  Call the DataAccess layer to retrive information about the wine.
  Returns LocationInventory object representing properties of the wine 
  that the IO layer uses to list the wine.
  
  Args:
    int locationID: The locationID of the wine being requested.
    int wineID: The wineID of the wine being requested.
    
  Return:
    LocationInventory: LocationInventory object of the wine.
                       Includes the information that will be displayed on the Inventory web page.
  """
  return dbGetWineUser(wineID, locationID)

def getWineGlobal(wine):
  """ Retrieves a wine from the global wine database 

  Calls the DataAccess layer to retrieve a global wine

  Args:
    int wine: The ID of the wine to retrieve
  Return:
    Wine: The wine retrieved
  """
  if DEBUG:
	  print "Calling dbGetWineGlobal"
  return dbGetWineGlobal(wine)


def getLocation(locationID,user):
  """Retrieve a location from the user's location map
  
  Call the DataAccess layer to retrieve a location.
  
  Args:
    int locationID: The locationID of the location.
    UserInfo user: A user object representing the user that owns
                   the location being retrieved.
    
  Return:
    LocationMap: LocationMap object of the location.
  """
  return dbGetLocation(locationID)

def getUserLocations(user):
  """Retrieve all the locations the user owns
  
  Call the DataAccess layer to retrieve a user's locations.
  
  Args:
    UserInfo user: A user object representing the user that owns
                   the location being retrieved.
    
  Return:
    list: A list of LocationMap objects representing the locations
          a user owns.
  """
  return dbGetUserLocations(user.userID)
  
def getLocationHistory(locationID, wineID):
  """Retrieve a location history 
  
  Call the DataAccess layer to retrieve a location history.
  
  Args:
    int locationID: The locationID of the location history.
    int wineID: The wineID of the location history.
    
  Return:
    LocationHistory: LocationHistory object of the location history.
  """
  return dbGetLocationHistory(locationID, wineID)
  

def getInventory(user):
  """Retrieve a user's inventory from database
  
  Return a list of LocationInventory objects representing the wines in a user's inventory.
  
  Args:
    UserInfo user: User whose inventory will be retrieved

  Return:
    list: A list of LocationInventory objects detailing the user's entire inventory. 
  """
  return dbGetInventory(user)

def getWideInventory(user):
  """Retrieve a user's inventory from database
  
  Return a list of wide objects representing the wines in a user's inventory.
  
  Args:
    UserInfo user: User whose inventory will be retrieved
    
  Return:
    list: A list of dicts representing all wines associated to a user
  """
  return dbGetWideInventory(user)

############# Add Methods #######################

def addLocationHistory(locationID, wineID, eventTag):
  """Add a Location History to the database.
  
  Call the DataAccess layer to insert a new Location History.
  
  Args:
    int locationID: The locationID of the location.
    int wineID: The wineID of the wine.
    string eventTag: Message detailing the event that occurred

  Return:
    LocationHistory: The LocationHistory added to the database
  """
  return dbAddLocationHistory(LocationHistory(None,locationID, wineID, str(datetime.datetime.now().replace(microsecond = 0)), eventTag))
  

def addWineUserByID(userWine, count, user):
  """Add a wine to user's inventory

  All fields are prespecified in userWine. Call DataAccess to add wine.

  Args:
    LocationInventory userWine: The representation of the wine to add, 
                                with fields filled out.
    int count: The number of wines to add
    UserInfo user: The user adding the wine.

  Return: 
    LocationInventory: The wine added to the database
  """
  addLocationHistory(userWine.li_locationID, userWine.li_wineID, "add-wine")
  
  return dbAddWineUser(userWine, count, user)

  
def addWineUser(wine, count,user, location = -1):

  """Add wine to user's inventory
  
  Call the DataAccess layer to insert the given wine into the specified inventory.
  If the wine doesn't exist already, generate a new wineID for it and assign its location. 
  If it does exist, increment its quantity. Update the Location History.
  
  Args:
    LocationInventory wine: A partially filled LocationInventory object representing the wine.
                            Not all the fields stored in the database have to be present,
                            such as li_locationID and li_wineID.
    int count: The quantity of this wine to add.
    UserInfo user: The user adding the wine.
    LocationMap location: The LocationMap object defining which inventory to insert in.
  """
  addLocationHistory(wine.li_locationID, wine.li_wineID, "add-wine")
  if location != -1:
    wine.li_locationID = location.locationID
  return dbAddWineUser(wine, count, user)
  
def moveWine(wine, location, count,user, copy = False):
  """Move a wine from one location to another
  
  Call the DataAccess layer to insert wines into location2. If copy is True, don't
  delete the wine from location1. Otherwise decrement the count of this wine in
  location1.
  Update the Location History.
  
  Args:
    LocationInventory wine: The LocationInventory object of the wine being moved.
    LocationMap location: The LocationMap object defining where to move the wine.
    int count: The number of wines to move. If more than the actual quantity, move all.
    bool copy: True if a copy of the wine is being stored in location, not the wine itself.
    UserInfo user: The user moving a wine
  Return:
    None
  """
  changes = {}
  # add the wine to the new location
  addWineUser(wine, count, location)
  if not copy:
    deleteWineUser(wine)
  else:
    # Decrement the count of the wine in it's original location by count
    changes['quantity'] = wine.quantity - count
    editEntryUser(wine,changes)
    
  # Update the location history
  addLocationHistory(location.locationID, wine.li_wineID, "move")

  
def getWinesByName(name):
  """Retrieve wines with the given name
  
      Call DataAccess layer to retrieve wines with a given name
  
      Args:
      string name: Name of wine
  
      Return:
      list: List of Wine objects having that name
  """
  return dbGetWinesByName(name)
  
def addWineGlobal(wine):
  """Add new wine to the global database

      Call the DataAccess layer to add a wine to the global database
      
      Args:
        Wine wine: Wine object of new wine

      Return:
        Wine: The wine added to the database
  """
  return dbAddWineGlobal(wine)

def editWineGlobal(wine):
  """Edit a wine in the global database

      Call the DataAccess layer to add a wine to the global database
      
      Args:
      Wine wine: Wine object of new wine

      Return:
        Wine: the wine that was edited
  """
  return dbEditWineGlobal(wine)


def addInventory(location):
  """Add inventory location to user's location map
  
  Call the DataAccess layer to create a new inventory location in the user's Location
  Map. Assign everything other than locationName and imagePath, which are already made. 
  Update the Location History.
  
  Args:
    LocationMap location: Partially filled LocationMap object that only defines locationName and
                          maybe imagePath.
  Return:
    LocationMap: The inventory added
  """
  # wine doesn't exist in this method so there is no wineID
  addLocationHistory(location.locationID, None, "add-location")
  return dbAddInventory(location)
  
def deleteWineUser(wine):
  """Delete wine from user's inventory
  
  Call the DataAccess layer to find a specified wine in the user's inventories and delete it.
  Update the Location History.
  
  Args:
    LocationInventory wine: The LocationInventory object of the wine being deleted.

  Return:
    LocationInventory: The wine deleted
  """
  if DEBUG:
	  print "Inventory: deleteWineUser is adding a location history"
  addLocationHistory(wine.li_locationID, wine.li_wineID, "delete-wine")
  if DEBUG:
	  print "Calling dbDeleteWineUser(wine)"
  return dbDeleteWineUser(wine)
  
  
def deleteInventory(location):
  """Delete user's inventory location
  
  Call the DataAccess layer to delete the location from the user's Location Map.
  Update the Location History.
  
  Args:
    LocationMap location: The LocationMap object of the location being deleted.

  Return:
    TODO
  """
  addLocationHistory(location.locationID, None, "delete-inventory")
  return dbDeleteInventory(location)

def editInventory(location, changes):
  """Edit a user's inventory
  
  Call the DataAccess layer to edit the properties of an inventory location. For every
  property specified in changes, replace the corresponding old property with the new one.
  Update the Location History.
  
  Args:
    LocationMap location: The LocationMap object of the location being modified.
    dict changes: A dictionary specifying properties and values of the form
                  {locationName:*, imagePath:*, etc}. Not all fields stored in the
                  database have to be present.

  Return:
    TODO
  """
  
  addLocationHistory(location.locationID, None, "edit-location")
  
  for key, value in changes.iteritems():
    location.__dict__[key] = value
  
  return dbEditInventory(location)
  
def editEntryUser(wine, changes):
  """Edit a wine in the user's inventory
  
  Call the DataAccess layer to edit the properties of a wine. For every property specified in
  changes, replace the corresponding old property with the new one. 
  Update the Location History.
  
  Args:
    LocationInventory wine: The LocationInventory object of the wine to be edited.
    dict changes: A dictionary specifying properties and values of the form
                  {li_locationID:*, quantity:*, etc}. Not all fields stored in the database
                  have to be present.
  Return:
    TODO
  """
  oldli = wine.li_locationID
  addLocationHistory(wine.li_locationID, wine.li_wineID, "edit-wine")
  print wine.li_locationID
  
  for key, value in changes.iteritems():
    wine.__dict__[key] = value
  
  return dbEditEntryUser(wine, oldli)


######################## BEGIN XML METHODS #################################

def importInventory(xfile):
  """Import a new inventory using an XML file
  
  NOTE: This feature is planned for a future release and as such this method is not 
         debugged or implemented.
  Call the DataAccess layer to create a new inventory and give it the properties detailed
  in the XML file.
  
  Args:
    XML xfile: The XML file. Specifies the properties of the
               inventory and the wines stored in it.  There should be enough information
               to fully generate an inventory.
   Here is the scheme I am using to build the xml:
   <Inventory username=$(UserName)>
    <Location location=$(locationID)>
      <$(wineID) location=$(locationID) ... for all the remaining attributes></$(wineID)>
      ... for all wines at that location
    </$(locationID)>
  </Inventory
  
  Better ways of organizing the info would be appreciated =)
  """
  #TODO: Standardize return according to Michael's error handling email
  #ignore namespaces
  parser.setFeature(feature_namespaces, 0)

    # Create the handler
  dh = XMLParser()

    # Tell the parser to use our handler
  parser.setContentHandler(dh)

    # Parse the input
    #is xfile is a path?
  if os.path.splitext(xfile) == ".xml":
    parser.parse(xfile)
    return self.inventory
  else:
    raise InvalidFileException
  
  #if that's just a string
  #only one of these if blocks would really be used
  #once that question is cornered
  if xfile.endsWith(".xml"):
    parser.parse(xfile)
    return self.inventory
  raise InvalidFileException
  
def makeXMLAttribute(attributeName, attributeData):
  """   NOTE: This feature is planned for a future release and as such this method is not 
         debugged or implemented.
  """
  attribute = []
  
  attribute.append(" ")
  attribute.append(attributeName)
  attribute.append("=\"")
  attribute.append(attributeData)
  attribute.append("\" ")
  
  return ''.join(attribute)

def makeXMLLocationRow(inventoryLocation):
  """
  NOTE: This feature is planned for a future release and as such this method is not 
         debugged or implemented.
  
  Generates all the XML to represent the wines that
  a user has a particular location 
  """
  location = []
  
  location.append("<")
  location.append("Location ")
  locationAttribute = makeXMLAttribute("location", inventoryItem.locationName)
  location.append(locationAttribute)
  
  for wine in inventoryLocation.wineList:
    location.append("\t") #purtify
    location.append(makeXMLWineRow(wine))
  
  location.append(">")
  location.append("</")
  location.append(locationAttribute)
  location.append(">")
  
  #stitch everything together
  return ''.join(location)
    
def makeXMLWineRow(inventoryItem):
  """   NOTE: This feature is planned for a future release and as such this method is not 
         debugged or implemented.
  """
  xmlRow = []
  
  xmlRow.append("<")
  name = dbGetWineByID(inventoryItem.li_wineID)[0].name
  xmlRow.append(name)
  xmlRow.append(makeXMLAttribute("location", inventoryItem.li_locationID))
  xmlRow.append(makeXMLAttribute("quantity", inventoryItem.quantity))
  
  if inventoryItem.personalStarRating != None:
    xmlRow.append(makeXMLAttribute("personalStarRating", inventoryItem.personalStarRating))
  if inventoryItem.isWishList != None:
    xmlRow.append(makeXMLAttribute("wishList", inventoryItem.isWishList))
  if inventoryItem.bitter != None:
    xmlRow.append(makeXMLAttribute("bitter", inventoryItem.bitter))
  if inventoryItem.sweet != None:
    xmlRow.append(makeXMLAttribute("sweet", inventoryItem.sweet))
  if inventoryItem.sour != None:
    xmlRow.append(makeXMLAttribute("sour", inventoryItem.sour))
  if inventoryItem.salty != None:
    xmlRow.append(makeXMLAttribute("salty", inventoryItem.salty))
  if inventoryItem.chemical != None:
    xmlRow.append(makeXMLAttribute("chemical", inventoryItem.chemical))
  if inventoryItem.pungent != None:
    xmlRow.append(makeXMLAttribute("pungent", inventoryItem.pungent))
  if inventoryItem.oxidized != None:
    xmlRow.append(makeXMLAttribute("oxidized", inventoryItem.oxidized))
  if inventoryItem.microbiological != None:
    xmlRow.append(makeXMLAttribute("microbiological", inventoryItem.microbiological))
  if inventoryItem.floral != None:
    xmlRow.append(makeXMLAttribute("floal", inventoryItem.floral))
  if inventoryItem.spicy != None:
    xmlRow.append(makeXMLAttribute("spicy", inventoryItem.spicy))
  if inventoryItem.fruity != None:
    xmlRow.append(makeXMLAttribute("fruity", inventoryItem.fruity))
  if inventoryItem.vegetative != None:
    xmlRow.append(makeXMLAttribute("vegetative", inventoryItem.vegetative))
  if inventoryItem.nutty != None:
    xmlRow.append(makeXMLAttribute("nutty", inventoryItem.nutty))
  if inventoryItem.carmelized != None:
    xmlRow.append(makeXMLAttribute("carmelized", inventoryItem.carmelized))
  if inventoryItem.woody != None:
    xmlRow.append(makeXMLAttribute("woody", inventoryItem.woody))
  if inventoryItem.eathy != None:
    xmlRow.append(makeXMLAttribute("eathy", inventoryItem.eathy))
  
  xmlRow.append(">")
  xmlRow.append("</")
  xmlRow.append(name)
  xmlRow.append(">")
  
  return ''.join(xmlRow)

def core(user):
  """   NOTE: This feature is planned for a future release and as such this method is not 
         debugged or implemented.
  """
  build = []
  
  build.append("Inventory name=")
  build.append(user.name)
  build.append("\"> ")
  
  return ''.join(build)
  
def makeHeader(user):
  """   NOTE: This feature is planned for a future release and as such this method is not 
         debugged or implemented.
  """
  header = []
  
  header.append("<")
  header.append(core(user))
  
  return ''.join(header)
  
def makeFooter(user):
  """   NOTE: This feature is planned for a future release and as such this method is not 
         debugged or implemented.
  """
  footer = []
  
  footer.append("</")
  footer.append(core(user))
  
  return ''.join(footer)

def exportInventory(location):
  """Export an XML representation of an inventory

  NOTE: This feature is planned for a future release and as such this method is not 
         debugged or implemented.
  
  
  Call the DataAccess layer to retrieve information about an inventory. Generate an XML file 
  representation of 
  the data. Retrieve all the properties of the inventory location and wines
  contained in it.
  Here's a sketch for how the xml may look
  
  <Inventory username=$(UserName)>
    <Location location=$(locationID)>
      <$(wineID) location=$(locationID) ... for all the remaining attributes></$(wineID)>
      ... for all wines at that location
    </$(locationID)>
  </Inventory
  
 Or perhaps simplier is better?
   <Inventory username=$(UserName)>
      <$(wineID) location=$(locationID) ... for all the remaining attributes></$(wineID)>
      ... for all wines at that location
  </$(UserName)Inventory
  
  Note: I have both written up
  
  Args:
    LocationMap location: The LocationMap object of the inventory location.
  
  Return:
    The XML representation of the inventory.
    OPTIONS TO CONSIDER: A link to a created XML, A string containing all the info
  """
  #TODO: Standardize returns
  #implementation of scheme #2 above
  inventory = dbGetUserLocations(user)[0]
  
  xml = []
  xml.append(makeHeader(user))
  for inventoryLocation in inventory:
    xml.append("/t")
    xml.append(makeXMLLocationRow(inventoryLocation))
    
  return ''.join(xml)

######################## END XML METHODS #################################

  
def viewStats(location, user):
    """Retrieve statistics about a  inventory:
      ~Red/White Wines
      ~Favorite Wines
      ~Favorite Flavors/Tags
      ~Total Wines in Inventory
      ~Wines with greatest quantity (Not currently displayed)

    Call the DataAccess layer to retrieve necessary information about an inventory. Construct
    a list detailing the information and return it.

    Args:
    LocationMap location: The LocationMap object of the location being analyzed.
     
    Return: displayInfo: A dictionary containing the information to be displayed:
        wineCount: Int number of wines
        redCount: Int number of red wines
        whiteCount: Int number of white wines
        rating1: Tuple - Top rated wine and rating
        rating2: Tuple - Second highest rated wine and rating
        rating3: Tuple - Third highest rated wine and rating
        aroma1: Tuple - String name of the favorite aroma and value
        aroma2: Tuple - String name of the second place aroma and value
        aroma3: Tuple - String name of the third place aroma and value
        quantity1: Tuple - Wine with the highest quantity and number
        quantity2: Tuple - Wine with the second highest quantity and number
        quantity3: Tuple - Wine with the third highest quantity and number
        locWines: List - 3 wines in this location
        history: List of 3 recent location histories
        size: Int number of wines in location

    """
    err = []
    sysErr = []


    displayInfo = {}

  
    userWineList = []    
    allUserWines = dbGetWideInventory(user)

    if allUserWines[0] == None:
      sysErr.append("Error getting user's wines")
      return (None, (err,sysErr))
    else:
      allUserWines = allUserWines[0]

    for userWine in allUserWines:
      if userWine['user_li_locationID'] == location.locationID:
        userWineList.append(userWine)

    # Check if location has wines
    if len(userWineList) == 0:
      noWineInfo = str(location.locationName) + ": No wines"
      return (noWineInfo, None)

    # Put 3 wines in locWines
    sampleWines = userWineList[:3]
    displayInfo['locWines'] = []
    for sampleWine in sampleWines:
      displayInfo['locWines'].append(sampleWine) 

    #Count the number of red and white wines in the user's inventory
    wineCount = 0
    redCount = 0
    whiteCount = 0
    i = 0
    for wine in userWineList:
      wineCount += wine['user_quantity']
      if wine['wine_wineType'] == 'Red':
        redCount += wine['user_quantity']
      elif wine['wine_wineType'] == 'White':
        whiteCount += wine['user_quantity']
      i += 1
        
    displayInfo['wineCount'] = wineCount
    displayInfo['redCount'] = redCount
    displayInfo['whiteCount'] = whiteCount

    #Sort wines by rating and choose the first three wines from the list for display
    userWineList.sort(key=lambda wine: wine['user_personalStarRating'], reverse = True)
    wine1 = dbGetWineByID(userWineList[0]['wine_wineID'])
    if wine1[0] == None:
      sysErr.append("Error getting favorite wines")
      return (None, (err,sysErr))
    else:
      wine1 = wine1[0]
      displayInfo['rating1'] = (userWineList[0], userWineList[0]['user_personalStarRating'])

    try:
      wine2 = dbGetWineByID(userWineList[1]['wine_wineID'])
      if wine2[0] == None:
        sysErr.append("Error getting favorite wines")
        return (None, (err,sysErr))
      else:
        wine2 = wine2[0]
        displayInfo['rating2'] = (userWineList[1], userWineList[1]['user_personalStarRating'])
    except:
      displayInfo['rating2'] = "None"

    try:
      wine3 = dbGetWineByID(userWineList[2]['wine_wineID'])
      if wine3[0] == None:
        sysErr.append("Error getting favorite wines")
        return (None, (err,sysErr))
      else:
        wine3 = wine3[0]
        displayInfo['rating3'] = (userWineList[2], userWineList[2]['user_personalStarRating'])
    except:
      displayInfo['rating3'] = "None"

    #Using above sorted list, take the favorite wines and take the average of their attributes

    aromas = [nameValue('chemical',0),nameValue('pungent',0),nameValue('oxidized',0),nameValue('microbiological',0),
              nameValue('floral',0),nameValue('spicy',0),nameValue('fruity',0),nameValue('vegetative',0),
              nameValue('nutty',0),nameValue('caramelized',0),nameValue('woody',0),nameValue('earthy',0)]

    for i in range(min(3, len(userWineList))):
      aromas[0].value = aromas[0].value + userWineList[i]['user_chemical']
      aromas[1].value = aromas[1].value + userWineList[i]['user_pungent']
      aromas[2].value = aromas[2].value + userWineList[i]['user_oxidized']
      aromas[3].value = aromas[3].value + userWineList[i]['user_microbiological']
      aromas[4].value = aromas[4].value + userWineList[i]['user_floral']
      aromas[5].value = aromas[5].value + userWineList[i]['user_spicy']
      aromas[6].value = aromas[6].value + userWineList[i]['user_fruity']
      aromas[7].value = aromas[7].value + userWineList[i]['user_vegetative']
      aromas[8].value = aromas[8].value + userWineList[i]['user_nutty']
      aromas[9].value = aromas[9].value + userWineList[i]['user_caramelized']
      aromas[10].value = aromas[10].value + userWineList[i]['user_woody']
      aromas[11].value = aromas[11].value + userWineList[i]['user_earthy']

    aromas[0].value = aromas[0].value / 3.0
    aromas[1].value = aromas[1].value / 3.0
    aromas[2].value = aromas[2].value / 3.0
    aromas[3].value = aromas[3].value / 3.0
    aromas[4].value = aromas[4].value / 3.0
    aromas[5].value = aromas[5].value / 3.0
    aromas[6].value = aromas[6].value / 3.0
    aromas[7].value = aromas[7].value / 3.0
    aromas[8].value = aromas[8].value / 3.0
    aromas[9].value = aromas[9].value / 3.0
    aromas[10].value = aromas[10].value / 3.0
    aromas[11].value = aromas[11].value / 3.0
    #Sort the averaged attributes and output the three that are closest to 1
    sorted(aromas, key=lambda a: a.value, reverse = True)
    displayInfo['aroma1'] = (str(aromas[0].name), int(aromas[0].value))
    displayInfo['aroma2'] = (str(aromas[1].name), int(aromas[1].value))
    displayInfo['aroma3'] = (str(aromas[2].name), int(aromas[2].value))
    
    #Sort wines by quantity and choose the first three wines from the list for display
    userWineList.sort(key=lambda wine: wine['user_quantity'], reverse = True)
    wine1 = dbGetWineByID(userWineList[0]['wine_wineID'])
    if wine1[0] == None:
      sysErr.append("Error getting favorite wines")
      return (None, (err,sysErr))

    else:
      wine1 = wine1[0]
      displayInfo['quantity1'] = (userWineList[0], int(userWineList[0]['user_quantity']))

    try:
      wine2 = dbGetWineByID(userWineList[1]['wine_wineID'])
      if wine2[0] == None:
        sysErr.append("Error getting favorite wines")
        return (None, (err,sysErr))

      else:
        wine2 = wine2[0]
        displayInfo['quantity2'] = (userWineList[1], int(userWineList[1]['user_quantity']))
    except:
      displayInfo['quantity2'] = "None"

    try:
      wine3 = dbGetWineByID(userWineList[2]['wine_wineID'])
      if wine3[0] == None:
        sysErr.append("Error getting favorite wines")
        return (None, (err,sysErr))

      else:
        wine3 = wine3[0]
        displayInfo['quantity3'] = (userWineList[2], int(userWineList[2]['user_quantity']))
    except:
      displayInfo['quantity3'] = "None"

    # Get recent history
    history = dbGetHistoryByLocation(location)
    if history[0] == None:
      sysErr.append("Error getting history")
      return (None, (err, sysErr))
    else:
      history = history[0]

    history.sort(key=lambda hist: hist.timestamp)

    history = history[:3]
    displayInfo['history'] = history

    #Calculate the total number of wines in the inventory
    quantity = 0
    for wine in userWineList:
      if wine['user_quantity'] != None:
        quantity = quantity + int(wine['user_quantity'])

    displayInfo['size'] = quantity

    return (displayInfo, None)

 
def viewArchive(location):
    """Retrieve the archive of a user's inventory

    Call the DataAccess layer to retrieve details about the inventory's archive. Return the 
    necesary information as a dict.

    Args:
    LocationMap location: The LocationMap object of the inventory location.

    Return:
    list: A list of LocationHistory objects.
    """
    return dbGetHistoryByLocation(location)

  
def rateWineUser(wine, rating):
    """Store user's rating of wine in database

    Call the DataAccess layer to store the wine's rating in the user's inventory.
    Update the Location History.

    Args:
    LocationInventory wine: The LocationInventory object of the wine to be rated.
    int rating: The rating on a 1-5 scale.

    Return:
      TODO
    """
    wine.personalStarRating = rating
    return dbEditEntryUser(wine)

class nameValue:
    """ This class is used to sort aromas in the viewStats method.
        Object containing a wine object and its corresponding distance to the seed
        Need this to be able to sort wines by distance, using the sorted() function
        Instance Variables:
        Wine wine: a wine object
        float distance: distance from this wine to the closest seed
        """
    def __init__(self, name, value):
        self.name = name
        self.value = value