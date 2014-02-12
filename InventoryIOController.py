"""Inventory system IO module: performs validation on input and constructs objects to pass to the next Controller Layer
"""
 
import re
from datetime import *
from Classes import *
from InstantiationValidation import *
import Globals
from InventoryController import *
from WineVectorGenerator import *

DEBUG = False

"""
NOTE: All methods prepended by input return a tuple of:
(object, tuple) - an object and an error tuple
(None, tuple) - None and an error tuple for user and system errors

NOTE: Dict arguments: These must be dicts but the dict may be empty or may
                      not have all of the the necessary information needed
                      to create the appropriate object.
      Non-dict arguments: These are supposed to be of the type that is
                          listed in the comments but this is not guaranteed.
                          To make up for this the validation methods
                          check everything to make sure it is of the
                          proper type before proceeding to use it.

"""

################# Getter Methods ##################

def inputGetWine(locationID, wineID, user):
  """Preprocess retrieval of wine from user's inventory
  
  Validate the IDs passed in then call the next lower layer to retrive
  information about the wine. Returns a tuple of a  LocationInventory object
  (or None if an error occured)representing properties of the wine that the
  IO layer uses to list the wine and an error tuple.
  
  Args:
    int locationID: The locationID of the wine being requested.
    int wineID: The wineID of the wine being requested.
    
  Return:
    A tuple of the following:
      LocationInventory: LocationInventory object of the wine.
      tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  # Make an empty error list
  err = []

  # validate the IDs
  validateID(locationID, err)
  validateID(wineID, err)

  if DEBUG:
  	print "inputGetWine: Checked ids"

  # Check if the user owns the location with locationID
  locations = inputGetUserLocations(user)

  if locations[0] == None:
    return locations
  else:
    locations = locations[0]

  if DEBUG:
  	print  "inputGetWine: Got the locations"

  isUserLocation = False
  if DEBUG:
    print "inputGetWine: locationID passed in is " + str(locationID)
  for userLoc in locations:
    if DEBUG:
	    print "Checking user location of " + str(userLoc.locationID)
    if userLoc.locationID == locationID:
      isUserLocation = True

  if DEBUG:
    print "checked the user locations"

  if not isUserLocation:
    err.append("Location does not belong to user")
    return (None, (err, None))
    

  # if there are no errors proceed
  if not err:
    return getWine(locationID,wineID)
  # There are errors. Return without making an object or getting a wine.
  else:
    return (None, (err, None))

def inputGetWineGlobal(wineID):
  """ Retrieves a wine from the global wine database 

  Calls the DataAccess layer to retrieve a global wine

  Args:
    int wineID: The ID of the wine to retrieve
  Return:
    Wine: The wine retrieved
  """
  if DEBUG:
    print "InventoryIOController: inputGetWineGlobal"

  err = []

  validateID(wineID,err)

  if not err:
    if DEBUG:
	    print "InventoryIOController: calling getWineGlobal(wineID)"
    return getWineGlobal(wineID)
  else:
    return (None,(err,None))

def inputGetWinesByAttr(attributes):
  """Preprocess retrieval of wines with qualities 
  similar to attributes

  Arg:
      dict attributes - a dictionary of a wine's attributes

  Return:
    A tuple of the following:
      list: List of close Wine objects
      tuple: a tuple consisting of a list of user errors and a list of system
             errors.
  """
  err = []

  validateAttr(attributes,err)
  
  if not err:
    return getWinesByAttr(attributes)
  
  
  
def inputGetWinesByName(name):
  """Preprocess retrieval of wines with the given name

  Args:
    str name: The name of the wine to retrieve
  Return:
    list: A list of wines that match that name
  """
  err = []
  
  return getWinesByName(name)
  
  
def inputAddWineGlobal(dictWine):
  """Preprocess addition of new wine to the global database

  Make a wine object and then pass it to the next lower layer.

  Args:
    dict dictWine: A dictionary of all the wine's attributes

  Return:
    Wine: The wine added to the global database.
  """
  err = []
  
  wine = makeWine(dictWine,True, err)[0]

  if not err:
    return addWineGlobal(wine)
  else:
    return  (None, (err, None))

def inputEditWineGlobal(dictWine):
  """Preprocess editing of a wine in the global database
      
  Args:
    Wine wine: Wine object of new wine

  Return:
    Wine: the wine that was edited
  """
  err = []


  if DEBUG:
    print 'fetching existing wine object for editing'
  wine = inputGetWineGlobal(int(dictWine['wineID']))

  if wine[1] != None and wine[1][0] != None:
      for error in wine[1][0]:
        print 'Error: ' + error

  if wine[1] != None and wine[1][1] != None:
    for error in wine[1][1]:
      print 'SysError: ' + error
  
  if DEBUG:
    print 'Updating wine values with those form the edit dictionary'
  for key, value in dictWine.iteritems():
    wine[0].__dict__[key] = value

  if not err:
    return editWineGlobal(wine[0])
  else:
    return  (None, (err, None))
  


def inputGetLocation(locationID,user):
  """Preprocess retrieval of a location from the user's location map
  
  Validate the locationID then call the next lowest layer to retrieve a
  location. 
  
  Args:
    int locationID: The locationID of the location.
    UserInfo user: The user getting this location.
    
  Return:
    A tuple of the following:
      LocationMap: LocationMap object of the location.
      tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  if DEBUG:
    print "in inputGetLocation"

  # Make an empty error list
  err = []

  # validate the ID
  validateID(locationID, err)

  # Check if the user owns the location with locationID
  locations = inputGetUserLocations(user)

  if DEBUG:
    print "In inputGetLocation got the user locations"

  if locations[0] == None:
    return locations
  else:
    locations = locations[0]

  isUserLocation = False
  for userLoc in locations:
    if userLoc.locationID == locationID:
      isUserLocation = True

  if not isUserLocation:
    err.append("Location does not belong to user")
    return (None, (err, None))

  if DEBUG:
    print "Checked if the user owned it"

  # if there are no errors proceed
  if not err:
    if DEBUG:
      print "calling get Location"
    return getLocation(locationID,user)
  # There are errors. Return without making an object or calling lower layers.
  else:
    return (None, (err, None))

def inputGetUserLocations(user):
  """Get a list of locations that belong to the user

  There is nothing to validate so call this calls the next lowest layer
  
  Args:
    None.
    
  Return:
    A tuple of:
      list: A list of LocationMap objects representing the user's locations.
      tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  return getUserLocations(user)


def inputGetLocationHistory(locationID, wineID,user):
  """Preprocess retrieval of a location history 

  Validate the IDs then call the next lowest layer to
  retrieve a location history.
  
  Args:
    int locationID: The locationID of the location history.
    int wineID: The wineID of the location history.
    UserInfo user: The user getting this location
    
  Return:
    A tuple of:
      LocationHistory: LocationHistory object of the location history.
      tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  # Make an empty error list
  err = []

  # validate the IDs
  validateID(locationID, err)
  validateID(wineID, err)

  # Check if the user owns the location with locationID
  locations = inputGetUserLocations(user)

  if locations[0] == None:
    return locations
  else:
    locations = locations[0]

  isUserLocation = False
  for userLoc in locations:
    if userLoc.locationID == locationID:
      isUserLocation = True

  if not isUserLocation:
    err.append("Location does not belong to user")
    return (None, (err, None))

  # if there are no errors proceed
  if not err:
    return getLocationHistory(locationID,wineID)
  # There are errors. Return without making an object or calling lower layers.
  else:
    return (None, (err, None))

 
def inputGetInventory(user):
  """Preprocess retrieval of user's inventory
  
  There is nothing to validate so this calls the next lowest layer.
  
  Args:
    UserInfo user: User whose inventory will be retrieved
    
  Return:
    list: A list of LocationInventory objects detailing the user's entire
          inventory.
    tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  # There is nothing to validate. Pass to the next layer.
  return getInventory(user)

def inputGetWideInventory(user):
  """Preprocess retrieval of user's wide inventory
  
  There is nothing to validate so this calls the next lowest layer.
  
  Args:
    UserInfo user: User whose inventory will be retrieved
    
  Return:
    list: A list of dicts representing wines in the user's inventory
    tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  return getWideInventory(user)


def inputViewStats(location,user):
  """Preprocess retrieval of statistics about an inventory:
      ~Red/White Wines
      ~Favorite Wines
      ~Favorite Flavors/Tags
      ~Total Wines in Inventory
      ~Number of Wines in each Location (Not currently used)
      ~Wines with greatest quantity (Not currently used)

  Args:
    LocationMap location: The LocationMap object of the location being analyzed.
    UserInfo user: The user whose inventory statistics will be displayed
    
  Return:
    TODO
    viewStats(): list of tuples containing the above information to be displayed
  """
  # Make an empty error list
  err = []

  # Check if the user owns the location with locationID
  locations = inputGetUserLocations(user)

  if locations[0] == None:
    err.append("Error getting user locations")
    return (None, (err, None))
  else:
    locations = locations[0]

  isUserLocation = False
  for userLoc in locations:
    if userLoc.locationID == location.locationID:
      isUserLocation = True

  if not isUserLocation:
    err.append("Location does not belong to user")
    return (None, (err, None))

  # if there are no errors proceed
  if not err:
    return viewStats(location,user)
  # There are errors. Return without making an object or calling lower layers
  else:
    return (None, (err, None))
  
def inputViewArchive(locationID,user):
  """Preprocess retrieval of the archive of a user's inventory
  
  Args:
    int  locationID: The LocationMap object of the inventory location.
    UserInfo user: The user that is viewing their archive.
    
  Return:
    list: A list of LocationHistory objects.
  """
  # Make an empty error list
  err = []

  # Check if the user owns the location with locationID
  locations = inputGetUserLocations(user)

  if locations[0] == None:
    return locations
  else:
    locations = locations[0]

  isUserLocation = False
  for userLoc in locations:
    if userLoc.locationID == locationID:
      isUserLocation = True

  if not isUserLocation:
    err.append("Location does not belong to user")
    return (None, (err, None))

  # Make a wine object while checking attributes for erros
  location = inputGetLocation(locationID,user)

  if location[0] == None:
    return location
  else:
    location = location[0]

  # if there are no errors proceed
  if not err:
    return viewArchive(location)
  # There are errors. Return without making an object or calling lower layers
  else:
    return (None, (err, None))


################ Adder Methods ###################
  

def inputAddWineUserByID(wineID, count, locationID, user):
  """Preprocess addition of global wine to user's inventory.

  Validate the IDs and the count then retrive global wine.
  Modify it to match InventoryLocation class fields then call the 
  next layer to add the wine.

  Args:
    int wineID: The global id of the wine
    int count: How many of the wine to add
    int locationID: The locationID of where to add the wine
    UserInfo user: object representing properties of the user

  Return:
    A tuple of:
      TODO
      tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  err = []

  validateID(wineID,err)
  validateID(locationID,err)

  if DEBUG:
    print "We validated the wineID"
    print err 

  if not err:
    pass
  else:
    return (None, (err,None))

  # Check if the user owns the location with locationID
  locations = inputGetUserLocations(user)

  if locations[0] == None:
    return locations
  else:
    locations = locations[0]

  isUserLocation = False
  for userLoc in locations:
    if userLoc.locationID == locationID:
      isUserLocation = True

  if not isUserLocation:
    err.append("Location does not belong to user")
    return (None, (err, None))

  wine = inputGetWineGlobal(wineID)[0]

  userWine = LocationInventory(li_locationID = locationID, li_wineID = wineID, quantity = count, tags = wine.tags, description = wine.description, imagePath = wine.imagePath, isWishlist = True, bitter = wine.bitter, sweet = wine.sweet, sour = wine.sour, salty = wine.salty, chemical = wine.chemical, pungent = wine.pungent, oxidized = wine.oxidized, microbiological = wine.microbiological, floral = wine.floral, spicy = wine.spicy, fruity = wine.fruity, vegetative = wine.vegetative, nutty = wine.nutty, caramelized = wine.caramelized, woody = wine.woody, earthy = wine.earthy)
  return addWineUserByID(userWine, count, user)
  
def inputAddWineUser(dictWine, count, locationID,user):
  """Preprocess addition of wine to user's inventory

  Validate the attributes in dictWine and create a wine object.
  Validate the locationID.
  Validate count.
  Pass these objects to the next lower layer.
  
  Args:
    dict dictWine: A dict representing the wine with format similar to the class' instance variables.
               Not all the fields stored in the database have to be present,
               such as li_locationID .
    int count: The quantity of this wine to add.
    int locationID: The ID of the location to add the wine to.
    UserInfo user: The user adding this wine.

  Return:
      TODO
      tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  # Make an empty error list
  err = []

  if DEBUG:
    print " we got to making an error dictionary"

  # validate the count
  validateCount(count, err)

  if DEBUG:
    print "Immediatley after eror validation"

  # Check if the user owns the location with locationID
  locations = inputGetUserLocations(user)

  if locations[0] == None:
    return locations
  else:
    locations = locations[0]

  isUserLocation = False
  for userLoc in locations:
    if userLoc.locationID == locationID:
      isUserLocation = True

  if not isUserLocation:
    err.append("Location does not belong to user")
    return (None, (err, None))

  if not err:
    pass
  else:
    return (None, (err,None))

  if DEBUG:
    print "Validated the ids"

  dictWine['li_locationID'] = locationID
  dictWine['quantity'] = count

  if DEBUG:
    print "Added to dictWine"

  # Make a wine object while checking attributes for erros
  wine = makeWine(dictWine,False, err)

  if DEBUG:
    print " In inputAddWineUser made a wine obj"
    print "Wine is: " + str(wine)

  if wine[0] == None:
    if DEBUG:
      print "RETURNING"
    return wine 
  else:
    wine = wine[0]

  if DEBUG:
    print wine.__dict__
    print "Getting a location of id: " + str(locationID)

  # Make a location object while checking attributes for errors
  location = inputGetLocation(locationID,user)

  if DEBUG:
    print "In inputAddWineUser got a location: " + str(location)

  if location[0] == None:
    return location
  else:
    location = location[0]

  if DEBUG:
    print "Wine is: " + str(wine)

  # if there are no errors proceed
  if not err:
    if DEBUG:
      print "calling the lower layers"
    return addWineUser(wine, count, location)
  # There are errors. Return without making an object or calling lower layers
  else:
    return (None, (err, None))
  
  
def inputAddInventory(user, dictLocation):
  """Preprocess addition of storage location to user's inventory
  
  Validate the attributes in dictLocation and create a location object.
  Pass this object to the next lower layer.
   
  Args:
    UserInfo user: UserInfo object of the user.
    dict dictLocation: dict that defines the attributes of the inventory to be added.

  Return:
      tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  if DEBUG:
    print "inputAddInventory"
  # Make an empty error list
  err = []

  if DEBUG:
    print "Starting inputAddInventory"

  # Make a location object while checking attributes for errors
  location = makeLocation(dictLocation, err)

  if DEBUG:
    print "Location made"

  if not err:
    if location.lm_userID == None:
      location.lm_userID = user.userID
  else:
    if DEBUG:
      print "Errors found"
    return (None, (err,None))

  # if there are no errors proceed
  if not err:
    if DEBUG:
      print "calling next layer"
    return addInventory(location)
  # There are errors. Return without making an object or calling lower layers
  else:
    return (None, (err, None))


################# Deletion Methods #########################
    
    
def inputDeleteWineUser(user, wineID, locationID):
  """Preprocess deletion of wine from user's inventory

  Validate the wine ID and the location ID.
  Pass these objects to the next lower layer.
  
  Args:
    UserInfo user: UserInfo object representing the user.
    int wineID: The id of the wine being deleted.
    int locationID: The id of the location the wine is in.

  Return:
      TODO
      tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  if DEBUG:
    print "InventoryIOController: entered inputDeleteWineUser"
    print "LocationID is " + str(locationID)
    print "WIne ID is " + str(wineID)

  # Make an empty error list
  err = []

  validateID(locationID,err)

  if DEBUG:
    print "inputDeleteWineUser: validated the ID"

  if not err:
    pass
  else:
    return (None,(err,None))

  # Make a wine object while checking attributes for erros
  wine = inputGetWine(locationID,wineID,user)

  if wine[0] == None:
    return wine
  else:
    wine = wine[0]


  if DEBUG:
  	print "inputDeleteWineUser: made a wine object"

  # if there are no errors proceed
  if not err:
    if DEBUG:
      print "InvetoryIO: calling deleteWineUser"
    return deleteWineUser(wine)
  # There are errors. Return without making an object or calling lower layers
  else:
    return (None, (err, None))
   
   
def inputDeleteInventory(locationID,user):
  """Preprocess deletion of user's inventory location
  
  Args:
    int locationID: The ID of the location to be deleted

  Return:
      TODO
      tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  if DEBUG:
    print "\t\tinputDeleteInventory"
  # Make an empty error list
  err = []

  # Check if the user owns the location with locationID
  locations = inputGetUserLocations(user)

  if locations[0] == None:
    return locations
  else:
    locations = locations[0]

  isUserLocation = False
  for userLoc in locations:
    if userLoc.locationID == locationID:
      isUserLocation = True

  if not isUserLocation:
    err.append("Location does not belong to user")
    return (None, (err, None))

  if DEBUG:
    print "Checked user locations"
             
  # Make a location object while checking attributes for errors
  location = inputGetLocation(locationID,user)

  if location[0] == None:
    return location
  else:
    location = location[0]

  if DEBUG:
    print "Checked this location"

  # if there are no errors proceed
  if not err:
    if DEBUG:
	    print "callding deleteInventory"
    return deleteInventory(location)
  # There are errors. Return without making an object or calling lower layers
  else:
    return (None, (err, None))

################# Edit Methods ########################

def inputRateWineUser(locationID, wineID, rating,user):
  """Preprocess storing user's rating of wine in database
  
  Args:
    int locationID: The ID of the location the wine is in.
    int wineID: The ID of the wine that the user is rating.
    int rating: The rating on a 1-5 scale.
    UserInfo user: The user that is rating this wine

  Return:
    TODO
  """
  # Make an empty error list
  err = []

  # Check if the user owns the location with locationID
  locations = inputGetUserLocations(user)

  if locations[0] == None:
    return locations
  else:
    locations = locations[0]

  isUserLocation = False
  for userLoc in locations:
    if userLoc.locationID == locationID:
      isUserLocation = True

  if not isUserLocation:
    err.append("Location does not belong to user")
    return (None, (err, None))

  # Make a wine object while checking attributes for erros
  wine = inputGetWine(locationID, wineID,user)

  if wine[0] == None:
    return wine
  else:
    wine = wine[0]

  # validate rating
  if rating == None:
    err.append('rating' + ' ' + 'None')
  elif not isinstance(rating, (long, int)):
    err.append('rating' + ' ' + 'Type')
  elif rating < 1 or rating > 5:
    err.append('rating' + ' ' + 'Range')

  # if there are no errors proceed
  if not err:
    return rateWineUser(wine,rating)
  # There are errors. Return without making an object or calling lower layers
  else:
    return (None, (err, None))


def inputMoveWine(wineID, locationID, count,user, copy = False):
  """Preprocess moving a wine from one location to another

  Validate the IDs and the count.
  Pass these objects to the next lower layer.
  
  Args:
    int wineID: The LocationInventory object of the wine being moved.
    int locationID: The LocationMap object defining where to move the wine.
    int count: The number of wines to move. If more than the actual quantity, move all.
    UserInfo user: A UserInfo object representing
    bool copy: True if a copy of the wine is being stored in location, not the wine itself.

  Return:
      TODO
      tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  if DEBUG:
    print "We're in inputMoveWine"
  # Make an empty error list
  err = []

  validateID(wineID,err)
  validateID(locationID,err)

  if DEBUG:
    print "We validated the wineID"
    print err 

  # Check if the user owns the location with locationID
  locations = inputGetUserLocations(user)

  if locations[0] == None:
    return locations
  else:
    locations = locations[0]

  isUserLocation = False
  for userLoc in locations:
    if userLoc.locationID == locationID:
      isUserLocation = True

  if not isUserLocation:
    err.append("Location does not belong to user")
    return (None, (err, None))

  if DEBUG:
    print "Checked user locations"

  # Make a location object while checking attributes for errors
  location = inputGetLocation(locationID,user)

  if location[0] == None:
    return location
  else:
    location = location[0]

  if not err:
    pass
  else:
    return (None,(err,None))

  # Make a wine object while checking attributes for erros
  wine = inputGetWine(locationID,wineID,user)

  if DEBUG:
    print "We got the wine"

  if wine[0] == None:
    return wine
  else:
    wine = wine[0]


  # validate the count
  validateCount(count, err)

  # if there are no errors proceed
  if not err:
    return moveWine(wine,location,count,user)
  # There are errors. Return without making an object or calling lower layers
  else:
    return (None, (err, None))

def inputEditInventory(locationID, changes,user):
  """Preprocess editing a user's inventory

  Check if a user is editing a location they own and then edit the 
  location.
  
  Args:
    int locationID: The ID of the location to edit.
    dict changes: A dictionary specifying properties and values of the form
                  {locationName:*, imagePath:*, etc}. Not all fields stored in the
                  database have to be present.
    UserInfo user: The user that owns the location.

  Return:
      TODO
      tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  if DEBUG:
    print "\t\tinputEditInventory"

  # Make an empty error list
  err = []

  # Check if the user owns the location with locationID
  locations = inputGetUserLocations(user)

  if locations[0] == None:
    return locations
  else:
    locations = locations[0]

  isUserLocation = False
  for userLoc in locations:
    if userLoc.locationID == locationID:
      isUserLocation = True

  if not isUserLocation:
    err.append("Location does not belong to user")
    return (None, (err, None))

  # Make a location object while checking attributes for errors
  location = inputGetLocation(locationID,user)
  if DEBUG:
    print "inputEditEntryUser got location"

  if location[0] == None:
    return location
  else:
    location = location[0]

  # if there are no errors proceed
  if not err:
    if DEBUG:
      print "Calling editInventory"
    return editInventory(location,changes)
  # There are errors. Return without making an object or calling lower layers
  else:
    return (None, (err, None))
  
  
def inputEditEntryUser(locationID, wineID, changes,user):
  """Preprocess editing a wine in the user's inventory

  Validate that the user is editing a wine in a location they own and then
  pass the changes in to edit the wine.
  
  Args:
    int locationID: The id of the location of the wine
    int wineID: The id of the wine to be edited.
    dict changes: A dictionary specifying properties and values of the form
                  {li_locationID:*, quantity:*, etc}. Not all fields stored in the database
                  have to be present.
    UserInfo user: The user that will be editing the wine.

  Return:
      TODO
      tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  # Make an empty error list
  err = []

  # Check if the user owns the location with locationID
  locations = inputGetUserLocations(user)

  if locations[0] == None:
    return locations
  else:
    locations = locations[0]

  isUserLocation = False
  for userLoc in locations:
    if userLoc.locationID == locationID:
      isUserLocation = True

  if not isUserLocation:
    err.append("Location does not belong to user")
    return (None, (err, None))

  # Make a wine object while checking attributes for erros
  wine = inputGetWine(locationID, wineID,user)

  if wine[0] == None:
    return wine
  else:
    wine = wine[0]

  # if there are no errors proceed
  if not err:
    if DEBUG:
      print "Calling editEntryUser"
    return editEntryUser(wine,changes)
  # There are errors. Return without making an object or calling lower layers
  else:
    return (None, (err, None))

################# Import/Export Methods #####################
  
def inputImportInventory(xfile):
  """Preprocess importing a new inventory using an XML file

  NOTE: This functionality is not currently implemented.
  
  Args:
    string xfile: The path to the XML file. Specifies the properties of the
               inventory and the wines stored in it.  There should be enough information
               to fully generate an inventory.


  Return:
      tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  # Make an empty error list
  err = []

  # if there are no errors proceed
  if not err:
    return importInventory(xfile)
  # There are errors. Return without making an object or calling lower layers
  else:
    return (None, (err, None))
  
  
def inputExportInventory(locationID,user):
  """Preprocess exporting an XML representation of an inventory

  NOTE: This functionality is postponed. It is not currently debugged or implemented.
  
  Args:
    LocationMap location: The LocationMap object of the inventory location.
  
  Return:
    The XML representation of the inventory.
    OPTIONS TO CONSIDER: A link to a created XML, A string containing all the info
  """
  # Make an empty error list
  err = []

  # Check if the user owns the location with locationID
  locations = inputGetUserLocations(user)

  if locations[0] == None:
    return locations
  else:
    locations = locations[0]

  isUserLocation = False
  for userLoc in locations:
    if userLoc.locationID == locationID:
      isUserLocation = True

  if not isUserLocation:
    err.append("Location does not belong to user")
    return (None, (err, None))

  # Make a wine object while checking attributes for erros
  location = inputGetLocation(locationID,user)

  if location[0] == None:
    return location
  else:
    location = location[0]

  # if there are no errors proceed
  if not err:
    return exportInventory(location)
  # There are errors. Return without making an object or calling lower layers
  else:
    return (None, (err, None))

