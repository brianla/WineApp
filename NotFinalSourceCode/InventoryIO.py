"""Inventory system IO module: performs validation on input and constructs objects to pass to the Controller Layer
"""
 
import re
from datetime import *
from Classes import *
import Globals
from Inventory import *
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

NOTE: The layer above this file is the routing layer (Init.py)
      The layer below this layer is the part of the controller (Inventory.py)

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
  if DEBUG:
    print "InventoryIO: inputGetWineGlobal"

  err = []

  validateID(wineID,err)

  if not err:
    if DEBUG:
	    print "InventoryIO: calling getWineGlobal(wineID)"
    return getWineGlobal(wineID)
  else:
    return (None,(err,None))


def inputGetLocation(locationID,user):
  """Preprocess retrieval of a location from the user's location map
  
  Validate the locationID then call the next lowest layer to retrieve a
  location. 
  
  Args:
    int locationID: The locationID of the location.
    
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
    TODO
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
    LocationMap location: The LocationMap object of the inventory location.
    
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

  
"""
NOTE: The Front End handles search. This method is no longer necessary.
def inputSearchInventory(dictWine):
  Preprocess searching through inventories for matching wine.

  Validate the attributes in dictWine. Create a wine object.
  Return a list of LocationInventory objects showing wines that fit the
  search parameters.
  
  Args:
    dictWine: A dict detailing properties of the wine to look for.
              Not all fields stored in the database have to be present.
               
  Return:
    A tuple of:
      list: A list of LocationInventory objects of wines matching the search parameters.
      tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  
  # Make an empty error list
  err = []

  # Make a wine object while checking attributes for errors
  wine = makeWine(dictWine, err)

  # if there are no errors proceed
  if not err:
        return searchInventory(wine)
  # There are errors. Return without making an object or calling lower layers.
  else:
    return (None, (err, None))
"""

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

  Return:
      TODO
      tuple: An error tuple consisting of two lists, the first of which is user
             errors and the second of which is system errors.
  """
  # Make an empty error list
  err = []

  if DEBUG:
    print " we got to making an error dictionary"

  # validate the IDs 
  # TODO
  #validateID(locationID, err)
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
      print "OH nooo what happen"
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
    print "InventoryIO: entered inputDeleteWineUser"
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

  TODO
  
  Args:
    int locationID: The ID of the location to edit.
    dict changes: A dictionary specifying properties and values of the form
                  {locationName:*, imagePath:*, etc}. Not all fields stored in the
                  database have to be present.
    UserInfo user: The user that owns the location.

  Return:
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

  TODO
  
  Args:
    int locationID: The id of the location of the wine
    int wineID: The id of the wine to be edited.
    dict changes: A dictionary specifying properties and values of the form
                  {li_locationID:*, quantity:*, etc}. Not all fields stored in the database
                  have to be present.
    UserInfo user: The user that will be editing the wine.

  Return:
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

  NOTE: This functionality is not currently implemented.
  
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

############## Validation Methods #############################
"""
NOTE: Validation Methods insert three types of errors into err:
   'Type' - The attribute is of the wrong type. For example, the
            database expects a LocationInventory's personalStarRating
            to be an int. If it is a float, string, or anything other than
            an int this 'Type' error will be inserted into the user error list.
   'Range' - Continuing with the example above, a personalStarRating must be
             between 0 and 5. If it is negative, 6, or above this 'Range' error
             will be inserted into the user error list.
   'None' - The database requires certain columns to be non-null. In other words
            they must have a value. For example, a UserInfo object must have a
            userID. If a validation method finds attribute in a non-null column
            (or a key column - only "regular" columns may be null. See database schema)
            does not exist this 'None' error will be inserted into the error list.
"""

def validateID(ID,err):
  """ Validates an ID

  Validates either a wineID or a locationID. If either ID encounters an error
  the relevant value 'Type', 'Range', or 'None' is inserted into the error
  list prepended by 'ID'.

  Args:
    ID - an ID of unknown type.
    list err - an error list

  Return:
    None
  """
  # The ID must exist
  if ID == None:
    err.append('ID' + ' ' + 'None')
  # NOTE: The comparison to a long or an int is
  # because of this website: http://stackoverflow.com/questions/3501382/checking-whether-a-variable-is-an-integer-or-not
  # for use with Python 2.x. This type of comparison is used for
  # all the validation and object creation methods
  # The ID must be an int.
  elif not isinstance(ID, (long, int)):
    err.append('ID' + ' ' + 'Type')
  # The ID must be non-negative
  elif ID < 0:
    err.append('ID' + ' ' + 'Range')


def validateCount(count,err):
  """ Validates a wine count

  Validates a wine count, making sure it exists, is an int, and is non-negative.
  This method may insert a 'Type', 'Range', or 'None' error into the error list
  prepended by 'count'.

  Args:
    count - a count of unknown type
    list err - an error list

  Return:
    None
  """
  # The count must exist
  if count == None:
    err.append('count' + ' ' + 'None')
  # Count must be an int. See validateID() for info on "(long,int)"
  elif not isinstance(count, (long, int)):
    err.append('count' + ' ' + 'Type')
  # count must be non-negative
  elif count < 0:
    err.append('count' + ' ' + 'Range')

def validateKey(key, err):
  """ Validates a key

  NOTE: This method is currently not used.
  Validates a key, making sure it exists, and is a string matching on of the
  attributes of a wine. This method may insert a 'Type', 'Range', or 'None' error into the error list
  prepended by 'key'.

  Args:
    key - a key of unknown type
    list err - an error list

  Return:
    None
  """
  # The key must exist
  if key == None:
    err.append('key' + ' ' + 'None')
  # Key must be a string
  elif not isinstance(key, basestring):
    err.append('key' + ' ' + 'Type')
  # Key must match an attribute of the wine
  match = False
  if TODO:
    match = True
  if not match:
    err.append('key' + ' ' + 'Range')
    

############## Object Creation Methods ########################
"""
  Object Creation methods follow the same error standards as
  the validation methods. See above.
"""

def makeWine(dictWine,globalWine, err):
  """ Validates and makes a wine object.

  Validates all attributes in a wine object. Returns none at the first
  error encountered and only returns an object if no errors are encountered.
  This method may insert a 'Type', 'Range', or 'None') error into the error
  list prepended with the attributes name. For example, if quantity
  was passed in negative, 'quantity Range' would be appended to err.

  Args:
    dict dictWine - A dictionary of wine attributes. May not contain all
                    attributes needed to make a wine. Some attributes may
                    be of improper type or range.
    list err - an error list

  Return:
    LocationInventory - A wine object, fully validated. If an errors is
                        encountered None is returned instead.

  """

  # Initialize all attributes to None to give them the scope
  # needed to make a user outside of the try-except blocks
  # Only Location inventory
  li_index = None
  li_locationID = None
  li_wineID = None

  #Location Inventory and Wine
  quantity = None
  personalStarRating = None
  isWishlist = None
  tags = None
  description = None
  imagePath = None
  bitter = None
  sweet = None
  sour = None
  salty = None
  chemical = None
  pungent = None
  oxidized = None
  microbiological = None
  floral = None
  spicy = None
  fruity = None
  vegetative = None
  nutty = None
  caramelized = None
  woody = None
  earthy = None

  # Wine only
  wineName = dictWine['wineName']
  varietal = dictWine['varietal']
  winery = dictWine['winery']
  wineType = None
  vintage = dictWine['vintage']
  region = dictWine['region']
  clusterID = None
  CSO = None
  averageStarRating = None
  barcode = None

  

  if not globalWine:
    # Check the wine ID
    try:
      li_wineID = dictWine['li_wineID']
      # check that the location ID is a an int
      if not isinstance( li_wineID, (int,long)):
        err.append('li_wineID'+ ' ' + 'Type')
        return (None, (err,None))
      # check that the location ID is not negative
      if li_wineID < 0:
        err.append('li_wineID' + ' ' + 'Range')
        return (None, (err,None))
    # The wine ID must be non-null.
    except KeyError:
      err.append('li_wineID' + ' ' + 'None')
      return (None, (err,None))

  if not globalWine:

    # Check the location ID
    try:
      li_locationID = dictWine['li_locationID']
      # check that the location ID is a an int
      if not isinstance( li_locationID, (int,long)):
        err.append('li_locationID'+ ' ' + 'Type')
        return (None, (err,None))
      # check that the location ID is not negative
      if li_locationID < 0:
        err.append('li_locationID' + ' ' + 'Range')
        return (None, (err,None))
  # NOTE: A KeyError is raised if li_locationID is
  # not in dictWine. The database requires
  # li_locationID to be non-null so None is
  # returned if a KeyError is encountered.
  # Check if the location ID exists
  # The location ID must be non-null.
    except KeyError:
      err.append('li_locationID' + ' ' + 'None')
      return (None, (err,None))
  
  if DEBUG:
    print "\t\t Making a wine with quantity: " + str(dictWine['quantity'])
  
  # Check the quantity
  try:
    quantity = dictWine['quantity']
    # Check that the quantity is an int
    if not isinstance( quantity, (int,long)):
      err.append('quantity' + ' ' + 'Type')
      return (None, (err,None))
    # Check that the quantity is non-negative
    if quantity < 0:
      err.append('quantity' + ' ' + 'Range')
      return (None, (err,None))
  # Check if the quantity exists.
  # The quantity must be non-null.
  except KeyError:
    err.append('quantity' + ' ' + 'None')
    return (None, (err,None))
  
  # Check the personalStarRating
  try:
    personalStarRating = dictWine['personalStarRating']
    # Check that the personalStarRating is an int
    #if not isinstance( personalStarRating, (int,long)):
    #  err.append('personalStarRating' + ' ' + 'Type')
    #  return (None, (err,None))
    # Check that the personalStarRating is between
    # 0 an 5, inclusive
    if personalStarRating != None and ( int(personalStarRating) < 0 or int(personalStarRating) > 5) :
      err.append('personalStarRating' + ' ' + 'Range')
      return (None, (err,None))
  # Check if the personalStarRating exists.
  # The personalStarRating may be null.
  except KeyError:
    print "personal star rating the helll"
    personalStarRating = None
    
  
  # Check isWishlist
  try:
    isWishlist = dictWine['isWishlist']
    if not isinstance(isWishlist, bool):
      err.append('isWishlist' + ' ' + 'Type')
      return (None, (err,None))
    # There is not range to check for isWishlist
  # Check if isWishlist exists
  # isWishlist must be non-null
  except KeyError:
    err.append('isWishlist' + ' ' + 'None')
    return (None, (err,None))


  # Check tags
  try:
    tags = dictWine['tags']

  except KeyError:
    err.append('tags' + ' ' + 'None')
    return (None, (err,None))

  try:
    description = dictWine['description']

  except KeyError:
    err.append('desc')
    return (None, (err,None))

  try:
    imagePath = dictWine['imagePath']

  except KeyError:
    #TODO
    #err.append('image')
    pass
    #return (None, (err,None))


  # Convert tags into floats and assign them to wine
  wineFloats = convertTagsToVector(dictWine['tags'])
  dictWine['bitter'] = wineFloats[0]
  dictWine['sweet'] = wineFloats[1]
  dictWine['sour'] = wineFloats[2]
  dictWine['salty'] = wineFloats[3]
  dictWine['chemical'] = wineFloats[4]
  dictWine['pungent'] = wineFloats[5]
  dictWine['oxidized'] = wineFloats[6]
  dictWine['microbiological'] = wineFloats[7]
  dictWine['floral'] = wineFloats[8]
  dictWine['spicy'] = wineFloats[9]
  dictWine['fruity'] = wineFloats[10]
  dictWine['vegetative'] = wineFloats[11]
  dictWine['nutty'] = wineFloats[12]
  dictWine['caramelized'] = wineFloats[13]
  dictWine['woody'] = wineFloats[14]
  dictWine['earthy'] = wineFloats[15]

  # Check the bitter attribute
  try:
    bitter = dictWine['bitter']
    # Check that bitter is a float
    if not isinstance(bitter, float):
      err.append('bitter' + ' ' + 'Type')
      return (None, (err,None))
    # bitter may not be negative
    if bitter < 0:
      err.append('bitter' + ' ' + 'Range')
      return (None, (err,None))
  # Check that bitter exists.
  # bitter may be null.
  except KeyError:
    bitter = None
    
  # Check the sweet attribute
  try:
    sweet = dictWine['sweet']
    # Check that sweet is a float
    if not isinstance(sweet, float):
      err.append('sweet' + ' ' + 'Type')
      return (None, (err,None))
    # sweet may not be negative
    if sweet < 0:
      err.append('sweet' + ' ' + 'Range')
      return (None, (err,None))
  # Check that sweet exists.
  # sweet may be null.
  except KeyError:
    sweet = None
    
  # Check the sour attribute
  try:
    sour = dictWine['sour']
    # Check that sour is a float
    if not isinstance(sour, float):
      err.append('sour' + ' ' + 'Type')
      return (None, (err,None))
    # sour may not be negative
    if sour < 0:
      err.append('sour' + ' ' + 'Range')
      return (None, (err,None))
  # Check that sour exists.
  # sour may be null.
  except KeyError:
    sour = None
    
  # Check the salty attribute
  try:
    salty = dictWine['salty']
    # Check that salty is a float
    if not isinstance(salty, float):
      err.append('salty' + ' ' + 'Type')
      return (None, (err,None))
    # salty may not be negative
    if salty < 0:
      err.append('salty' + ' ' + 'Range')
      return (None, (err,None))
  # Check that salty exists.
  # salty may be null.
  except KeyError:
    salty = None
    
  # Check the chemical attribute
  try:
    chemical = dictWine['chemical']
    # Check that chemical is a float
    if not isinstance(chemical, float):
      err.append('chemical' + ' ' + 'Type')
      return (None, (err,None))
    # chemical may not be negative
    if chemical < 0:
      err.append('chemical' + ' ' + 'Range')
      return (None, (err,None))
  # Check that chemical exists.
  # chemical may be null.
  except KeyError:
    chemical = None
    
  # Check the pungent attribute
  try:
    pungent = dictWine['pungent']
    # Check that pungent is a float
    if not isinstance(pungent, float):
      err.append('pungent' + ' ' + 'Type')
      return (None, (err,None))
    # pungent may not be negative
    if pungent < 0:
      err.append('pungent' + ' ' + 'Range')
      return (None, (err,None))
  # Check that pungent exists.
  # pungent may be null.
  except KeyError:
    pungent = None
    
  # Check the oxidized attribute
  try:
    oxidized = dictWine['oxidized']
    # Check that oxidized is a float
    if not isinstance(oxidized, float):
      err.append('oxidized' + ' ' + 'Type')
      return (None, (err,None))
    # oxidized may not be negative
    if oxidized < 0:
      err.append('oxidized' + ' ' + 'Range')
      return (None, (err,None))
  # Check that oxidized exists.
  # oxidized may be null.
  except KeyError:
    oxidized = None
    
  # Check the microbiological attribute
  try:
    microbiological = dictWine['microbiological']
    # Check that microbiological is a float
    if not isinstance(microbiological, float):
      err.append('microbiological' + ' ' + 'Type')
      return (None, (err,None))
    # microbiological may not be negative
    if microbiological < 0:
      err.append('microbiological' + ' ' + 'Range')
      return (None, (err,None))
  # Check that microbiological exists.
  # microbiological may be null.
  except KeyError:
    microbiological = None
    
  # Check the floral attribute
  try:
    floral = dictWine['floral']
    # Check that floral is a float
    if not isinstance(floral, float):
      err.append('floral' + ' ' + 'Type')
      return (None, (err,None))
    # floral may not be negative
    if floral < 0:
      err.append('floral' + ' ' + 'Range')
      return (None, (err,None))
  # Check that floral exists.
  # floral may be null.
  except KeyError:
    floral = None
    
  # Check the spicy attribute
  try:
    spicy = dictWine['spicy']
    # Check that spicy is a float
    if not isinstance(spicy, float):
      err.append('spicy' + ' ' + 'Type')
      return (None, (err,None))
    # spicy may not be negative
    if spicy < 0:
      err.append('spicy' + ' ' + 'Range')
      return (None, (err,None))
  # Check that spicy exists.
  # spicy may be null.
  except KeyError:
    spicy = None
    
  # Check the fruity attribute
  try:
    fruity = dictWine['fruity']
    # Check that fruity is a float
    if not isinstance(fruity, float):
      err.append('fruity' + ' ' + 'Type')
      return (None, (err,None))
    # fruity may not be negative
    if fruity < 0:
      err.append('fruity' + ' ' + 'Range')
      return (None, (err,None))
  # Check that fruity exists.
  # fruity may be null.
  except KeyError:
    fruity = None
    
  # Check the vegetative attribute
  try:
    vegetative = dictWine['vegetative']
    # Check that vegetative is a float
    if not isinstance(vegetative, float):
      err.append('vegetative' + ' ' + 'Type')
      return (None, (err,None))
    # vegetative may not be negative
    if vegetative < 0:
      err.append('vegetative' + ' ' + 'Range')
      return (None, (err,None))
  # Check that vegetative exists.
  # vegetative may be null.
  except KeyError:
    vegetative = None
    
  # Check the nutty attribute
  try:
    nutty = dictWine['nutty']
    # Check that nutty is a float
    if not isinstance(nutty, float):
      err.append('nutty' + ' ' + 'Type')
      return (None, (err,None))
    # nutty may not be negative
    if nutty < 0:
      err.append('nutty' + ' ' + 'Range')
      return (None, (err,None))
  # Check that nutty exists.
  # nutty may be null.
  except KeyError:
    nutty = None
    
  # Check the caramelized attribute
  try:
    caramelized = dictWine['caramelized']
    # Check that caramelized is a float
    if not isinstance(caramelized, float):
      err.append('caramelized' + ' ' + 'Type')
      return (None, (err,None))
    # caramelized may not be negative
    if caramelized < 0:
      err.append('caramelized' + ' ' + 'Range')
      return (None, (err,None))
  # Check that caramelized exists.
  # caramelized may be null.
  except KeyError:
    caramelized = None
    
  # Check the woody attribute
  try:
    woody = dictWine['woody']
    # Check that woody is a float
    if not isinstance(woody, float):
      err.append('woody' + ' ' + 'Type')
      return (None, (err,None))
    # woody may not be negative
    if woody < 0:
      err.append('woody' + ' ' + 'Range')
      return (None, (err,None))
  # Check that woody exists.
  # woody may be null.
  except KeyError:
    woody = None
    
  # Check the earthy attribute
  try:
    earthy = dictWine['earthy']
    # Check that earthy is a float
    if not isinstance(earthy, float):
      err.append('earthy' + ' ' + 'Type')
      return (None, (err,None))
    # earthy may not be negative
    if earthy < 0:
      err.append('earthy' + ' ' + 'Range')
      return (None, (err,None))
  # Check that earthy exists.
  # earthy may be null.
  except KeyError:
    earthy = None

  if DEBUG:
    print li_locationID
    print li_wineID
    print quantity
    print tags
    print description
    print imagePath
    print personalStarRating
    print isWishlist
    print bitter
    print nutty
    print "Returning now"

  # No errors found. Return the wine object
  if not globalWine:
    wine = LocationInventory(li_index, li_locationID, li_wineID, quantity, tags, description,
                           imagePath, personalStarRating, isWishlist, bitter, sweet, sour,
                           salty, chemical, pungent, oxidized, microbiological,
                           floral, spicy, fruity, vegetative, nutty, caramelized,
                           woody, earthy)
  else:
    wine = Wine(None,wineName,varietal,winery,wineType,vintage,region,
                clusterID,CSO,tags,description,averageStarRating,imagePath,
                barcode,bitter,sweet,sour,salty,chemical,pungent,oxidized,
                microbiological,floral,spicy,fruity,vegetative,nutty,caramelized,
                woody,earthy)

  return (wine,(err,None))

def makeLocation(dictLocation, err):
  """ Validates and makes a location object.

  Validates all attributes in a location object. Returns none at the first
  error encountered and only returns an object if no errors are encountered.
  This method may insert a 'Type', 'Range', or 'None' error into the error
  dictionary prepended by the attributes name. For example, if locationID
  was passed in negative, a 'Range' error would be placed in err prepended by
  'locationID'.

  Args:
    dict dictLocation - A dictionary of location attributes. May not contain all
                    attributes needed to make a wine. Some attributes may
                    be of improper type or range.
    list err - an error list

  Return:
    LocationMap - A location object, fully validated. If an errors is
                  encountered None is returned instead.

  """
  # Initialize all attributes to None to give them the scope
  #   needed to make a user outside of the try-except blocks
  lm_userID = None  
  locationName = None
  timeCreated = None
  imagePath = None
  print "Making location"

  # Check the lm_userID
  try:
    print "Testing user id"
    lm_userID = dictLocation['lm_userID']
    # Check that the lm_userID is an int
    if not isinstance( lm_userID, (int,long)):
      err.append('lm_userID' + ' ' + 'Type')
      return (None, (err,None))
    # Check that the lm_userID is non-negative
    if lm_userID < 0:
      err.append('lm_userID' + ' ' + 'Range')
      return (None, (err,None))
      #print sys.exc_info()
  # Check if the lm_userID exists.
  # The lm_userID must be non-null.
  except KeyError: 
    #print "EXCEPTION in makeLocation: " + str(sys.exc_info())
    err.append('lm_userID' + ' ' + 'None')
    return (None, (err,None))

  if DEBUG:
    print "checked userID"

  # Check the locationName
  try:
    print "testing location name"
    locationName = dictLocation['locationName']
    # Check that the locationName is a string
    if not isinstance( locationName, basestring):
      err.append('locationName' + ' ' + 'Type')
      return (None, (err,None))
    # Check that the locationName is shorter than 255 characters
    if len(locationName) > 255:
      err.append('locationName' + ' ' + 'Range')
      return (None, (err,None))
  # Check if the locationName exists.
  # The locationName must be non-null.
  except KeyError:
    err.append('locationName' + ' ' + 'None')
    return (None, (err,None))

  if DEBUG:
    print "Checked location name"

  # Check the timeCreated
  try:
    print "testing time created"
    timeCreated = dictLocation['timeCreated']
    if DEBUG:
      print "Gunna try"
    # Check that the timeCreated is a valid timestamp
    try:
      #print timeCreated
      datetime.datetime.strptime(timeCreated, "%Y-%m-%d %H:%M:%S")
    except ValueError:
      err.append('timeCreated' + '' + 'Type')
    # There is no range to check for timeCreated
  # Check if the timeCreated exists.
  # The timeCreated must be non-null.
  except KeyError:
    err.append('timeCreated' + ' ' + 'None')
    return (None, (err,None))

  #print "Checked time created"
  # Check the imagePath
  try:
    print "testing image path"
    imagePath = dictLocation['imagePath']
    # Check that the imagePath is a string
    if not isinstance( imagePath, basestring):
      err.append('imagePath' + ' ' + 'Type')
      return (None, (err,None))
    # Check that the imagePath is shorter than 255 characters
    if len(imagePath) > 255:
      err.append('imagePath' + ' ' + 'Range')
      return (None, (err,None))
  # Check if the imagePath exists.
  # The imagePath may be null.
  except KeyError:
    imagePath = None

  if DEBUG:
    print "Checked image path"
    print "done making location"
  return LocationMap( None, lm_userID, locationName, timeCreated, imagePath)
