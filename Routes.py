from InventoryIOController import *
from RecommendIOController import *
from UserIOController import *
from WineIOController import *
from Classes import *
from InstantiationValidation import *
from Temp_SysTest import *
from VarietalMatch import *
from WineVectorGenerator import *
import os, binascii
import json
import datetime
import traceback
import sys
#from werkzeug import secure_filename #This probably isn;t needed


#CONSTANTS
USER_UPLOAD_FOLDER = 'static/images/user/'
WINE_UPLOAD_FOLDER = 'static/images/wine/'
LOCATION_UPLOAD_FOLDER = 'static/images/location/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = USER_UPLOAD_FOLDER

#SESSION MANAGER DICTIONARY
sessions = dict()

@app.route('/')
def index():
  """Load splash output page
  """

  #Steps:
  # if logged in redirect to profile
  # if not logged in display page


  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid != None and user != None:
    return redirect(url_for('inventory'))


  print 'Rendering Test Login Page'
  return render_template('index.html', user=user)


# User profile routing *****************************************************

@app.route('/User')
def user():
  """Load user profile page
  """
  #Steps:
  # if not logged in redirect to login
  # else display page
  print 'Accessing User Profile'

  #get from cookies
  sid = None
  if request.cookies != None:
    sid = request.cookies.get('wc_session_id')
  print 'Session ID = ' + str(sid)

  #get the user object if it exists
  user = getUserFromSession(sid)
  print 'UserObj = ' + str(user)

  #if user is None we need to redirect to login page
  if user == None:
    return redirect(url_for('index'))

  print 'Now trying to render template lawl'

  #Do stuff here
  print 'Email:' + user.emailAddress
  print 'Password:' + user.password

  print 'It actually printered'
  #profile = blahblahblah

  locations = inputGetUserLocations(user)[0]

  locsList = []  # Name, number of wines, list of wines 
  totalWineCount = 0
  totalRedCount = 0
  totalWhiteCount = 0
  totalLocCount = 0
  favoriteWines = []
  history = []
  favoriteAromas = []
  recommendedWines = []

  for loc in locations:
    totalLocCount += 1
    stat = inputViewStats(loc, user)[0]
    if type(stat) == str:
      continue

    
    locsList.append((loc.locationName.replace(chr(0xa0), ''), stat['wineCount'], stat['locWines']))

    totalWineCount += stat['wineCount']
    totalRedCount += stat['redCount']
    totalWhiteCount += stat['whiteCount']
    if stat['rating1'] != "None":
      favoriteWines.append(stat['rating1'])
    if stat['rating2'] != "None":
      favoriteWines.append(stat['rating2'])
    if stat['rating3'] != "None":
      favoriteWines.append(stat['rating3'])
    history += stat['history']
    favoriteAromas.append(stat['aroma1'])
    favoriteAromas.append(stat['aroma2'])
    favoriteAromas.append(stat['aroma3'])

  # Get top 3 favorite wines, recent history, and aromas
  favoriteWines.sort(key = lambda wine_rating: wine_rating[1], reverse = True)
  history.sort(key = lambda hist: hist.timestamp)
  favoriteAromas.sort(key = lambda aroma_val: aroma_val[1])

  count = 0
  favoriteWinesReal = []
  for wine in favoriteWines:
    if 2 < count:
      break
    favoriteWinesReal.append(wine[0])
    count += 1

  count = 0
  historyReal = []
  for hist in history:
    if 2 < count:
      break
    if hist.eventTag == 'add-wine':
      hist.eventTag = 'Added a new wine'
    elif hist.eventTag == 'move':
      hist.eventTag = 'Moved a wine to a different location'
    elif hist.eventTag == 'add-location':
      hist.eventTag = 'Added a new location'
    elif hist.eventTag == 'delete-wine':
      hist.eventTag = 'Deleted a wine'
    elif hist.eventTag == 'delete-inventory':
      hist.eventTag = 'Deleted an inventory'
    elif hist.eventTag == 'edit-location':
      hist.eventTag = 'Edited a location'
    elif hist.eventTag == 'edit-wine':
      hist.eventTag = 'Edited a wine\'s information'
    elif hist.eventTag == 'editEntryUser':
      hist.eventTag == 'Edited a wine\'s information'
    historyReal.append(hist)
    count += 1

  count = 0
  favoriteAromasReal = []
  for aroma in favoriteAromas:
    if 2 < count:
      break
    favoriteAromasReal.append(aroma[0])
    count += 1

  # Get recommendations
  shelf = inputGetUserShelves(user)[0]
  #if 0 < len(shelf):
    #shelf = shelf[0]
    #recommendations = inputRecommend(shelf.recommenderID, 3)[0]
  #else:
    #recommendations = []
  recommendations = []

  return render_template('profile_test.html', user=user, locsList = locsList, totalWineCount = totalWineCount, totalRedCount = totalRedCount, totalWhiteCount = totalWhiteCount, totalLocCount = totalLocCount, favoriteWines = favoriteWinesReal, favoriteAromas = favoriteAromasReal, recommendations = recommendations, history = historyReal)



@app.route('/User/login', methods = ["POST"])
def userLogin():
  """Login user
  """

  print '/User/login - Already Logged In'

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid != None and user != None:
    return redirect(url_for('inventory'))

  print '/User/login - Attempting to Login'

  #Extract the user variables
  email = sanitize(request.form['login_email'])
  password = sanitize(request.form['login_password'])

  try:
    user = inputLogin(email, password)

    sid = binascii.b2a_hex(os.urandom(15))
    sessions[str(sid)] = user[0]
    resp = make_response(redirect(url_for('inventory')))
    resp.set_cookie('wc_session_id', str(sid))
    print 'SessionID = ' + str(sid)

    print "Login Succeeded!"

    return resp

  except:
    ex, ex_type, tb = sys.exc_info()
    print ex
    print ex_type
    traceback.print_tb(tb)
    del tb
    return redirect(url_for('index'))

  #default fail
  return redirect(url_for('index'))



@app.route('/User/veriflogin', methods = ["POST"])
def userLoginVerif():

  print request.headers['Content-Type']

  #Make sure the request is a proper JSON request type
  #if request.headers['Content-Type'] == 'application/json':

  #Extract the user variables
  email = sanitize(request.form['email'])
  password = sanitize(request.form['password'])

  try:
    user = login(email, password)
    print str(user[0])
    if user[0] != None:
      print 'Valid User'
      print url_for('inventory')
      return jsonify(status = 'VALID', newurl = url_for('inventory'))
    else:
      print 'INVALID USER NULL VALUE'
      return jsonify(status = 'INVALID')

  except:
    print 'INVALID USER EXCEPTION'
    ex, ex_type, tb = sys.exc_info()
    print ex
    print ex_type
    traceback.print_tb(tb)
    del tb
    return jsonify(status = 'INVALID')
#else:
  print 'INVALID USER BAD REQUEST'
  return jsonify(status = 'INVALID')



@app.route('/User/logout')
def userLogout():
  """Logout user
  """
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid != None and user != None:
    del sessions[sid]

  return redirect(url_for('index'))




@app.route('/User/create', methods = ["POST"])
def userCreate():
  """Create user
  """

  print '/User/create - Now checking for Already Logged In'

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid != None and user != None:
    return redirect(url_for('inventory'))

  print '/User/create - Attempting to Create Account'

  #Extract the user variables
  user = dict()
  #user['userID'] = None
  user['emailAddress'] = str(sanitize(request.form['create_email']))
  user['password'] = str(sanitize(request.form['create_password']))
  user['name'] = str(sanitize(request.form['create_name']))
  user['location'] = str(sanitize(request.form['create_location']))
  if len(sanitize(request.form['create_birthday'])) > 0:
    user['dateOfBirth'] = str(sanitize(request.form['create_birthday']))


  print '/User/create - Dicts created, attempting to load image'

  #ProfileImage
  validImage = False
  if request.files != None:
    myFile = request.files['create_user_image']
    
    if myFile and allowed_file(myFile.filename):
      filename = binascii.b2a_hex(os.urandom(10)) + '.' + myFile.filename.rsplit('.', 1)[1]
      print filename
      user['imagePath'] = filename
      validImage = True


  print '/User/create - Image loaded'

  try:
    user = inputCreateUser(user)


    print '/User/create - Made it back from the depths of DataAccess'

    if user[1] != None and user[1][0] != None:
      for i in range(0, len(user[1][0])):
        print 'Error: ' + str(user[1][0][i])
      for j in range(0, len(user[1][1])):
        print 'SysError: ' + str(user[1][1][j])

    if user[0] == None:
      print 'Account creation failed'
      return redirect(url_for('index'))
    else:
      print "Account Creation Succeeded!"

    #Now that we have a valid account object, upload the image file
    if validImage:
      myFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    print 'Got passed image upload code'

    #And finally log the user in to the server
    user = inputLogin(user[0].emailAddress, user[0].password)

    print 'Got login user object'

  #  if user[1] != None and user[1][0] != None:
  #    for i in range(0, len(user[1][0])):
  #      print 'Error: ' + str(user[1][0])

    print 'Now making session keys'

    sid = binascii.b2a_hex(os.urandom(15))
    sessions[str(sid)] = user[0]
    resp = make_response(redirect(url_for('inventory')))
    resp.set_cookie('wc_session_id', str(sid))
    print 'SessionID = ' + str(sid)


    # Give user default shelves for white and red wines
    print user
    redChannelName = "Red Wines"
    whiteChannelName = "White Wines"
    redSeeds = [5, 6, 7, 19]
    whiteSeeds = [27, 55, 60, 88, 89]
    inputCreateChannel(user[0], redChannelName, redSeeds)
    inputCreateChannel(user[0], whiteChannelName, whiteSeeds)

    print "Login Succeeded!"

    return resp

  except:
    return redirect(url_for('index'))

  #default fail
  return redirect(url_for('index'))



@app.route('/User/verifcreate', methods = ["POST"])
def userVerifCreate():
  """Create user
  """
  email = sanitize(request.form['email'])

  try:
    exists = doesUserExist(email)
    print 'User Exists for email(' + email + '): ' + str(exists)
    if not exists:
      print 'Okay to use this email address'
      return jsonify(status = 'VALID')
    else:
      print 'THIS EMAIL ADDRESS IS IN USE'
      return jsonify(status = 'INVALID')

  except:
    print 'INVALID EMAIL EXCEPTION'
    return jsonify(status = 'INVALID')
#else:
  print 'INVALID CREATE USER - BAD REQUEST'
  return jsonify(status = 'INVALID')



@app.route('/User/edit', methods = ["POST"])
def userEdit():


  print '/User/edit - Now checking for Already Logged In'

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  print '/User/edit - Attempting to Edit Account'

  #Extract the user variables
  userDict = dict()
  #user['userID'] = None
  if len(sanitize(request.form['edit_password'])) > 0:
    userDict['password'] = str(sanitize(request.form['edit_password']))
  else:
    userDict['password'] = str(user.password)
  if len(sanitize(request.form['edit_name'])) > 0:
    userDict['name'] = str(sanitize(request.form['edit_name']))
  if len(sanitize(request.form['edit_location'])) > 0:
    userDict['location'] = str(sanitize(request.form['edit_location']))
  if len(sanitize(request.form['edit_birthday'])) > 0:
    userDict['dateOfBirth'] = str(sanitize(request.form['edit_birthday']))

  #ProfileImage
  validImage = False
  if request.files != None:
    myFile = request.files['edit_user_image']
    
    if myFile and allowed_file(myFile.filename):
      filename = binascii.b2a_hex(os.urandom(10)) + '.' + myFile.filename.rsplit('.', 1)[1]
      print filename
      userDict['imagePath'] = filename
      validImage = True



  try:
    #UPDATE USER HERE
    print 'About to Update Account Information'
    user = inputEditUser(getUserFromSession(sid), userDict)
    print 'Back from Account Update'
    print str(user)

    if user[1] != None and user[1][0] != None:
      for i in range(0, len(user[1][0])):
        print 'Error: ' + str(user[1][0])

    #Now that we have a valid account object, upload the image file
    if user[0] != None:
      if validImage:
        print 'Final File Path: ' + str(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        myFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

      resp = make_response(redirect(url_for('inventory')))
      return resp

  except:
    return redirect(url_for('index'))

  #default fail
  return redirect(url_for('index'))


@app.route('/User/verifedit', methods = ["POST"])
def userVerifEdit():

  email = sanitize(request.form['email'])
  password = sanitize(request.form['password'])

  try:
    user = inputLogin(email, password)
    if user[0] != None:
      return jsonify(status = 'VALID')
    else:
      print 'BAD USER/PASS VERIFICATION'
      return jsonify(status = 'INVALID')

  except:
    print 'INVALID USER/PASS EXCEPTION'
    return jsonify(status = 'INVALID')
#else:
  print 'INVALID EDIT USER - BAD REQUEST'
  return jsonify(status = 'INVALID')


"""
@app.route('/User/image_upload', methods=['POST'])
def user_image_upload():

  print 'Accessing User Image Upload'

  #get from cookies
  sid = None
  if request.cookies != None:
    sid = request.cookies.get('wc_session_id')
  print 'Session ID = ' + str(sid)

  #get the user object if it exists
  user = getUserFromSession(sid)
  print 'UserObj = ' + str(user)

  #if user is None we need to redirect to login page
  if user == None:
    return redirect(url_for('index'))

  file = request.files['user_image']
  if file and allowed_file(file.filename):
    filename = binascii.b2a_hex(os.urandom(10))

    #associate image name with userprofile

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    """


@app.route('/User/delete', methods=['POST'])
def userDelete():

  print '/User/delete - Now checking for Already Logged In'

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  print '/User/delete - Attempting to Delete Account'

  email = sanitize(request.form['email'])

  if email == user.emailAddress:
    try:
      print "Deleting"
      deletedUser = inputDeleteUser(user)
      if deletedUser[0] != None:
        del sessions[sid]
        return jsonify(status = 'VALID', newurl = url_for('index'))
      else:
        print 'BAD DELETE VERIFICATION'
        return jsonify(status = 'INVALID', newurl = url_for('index'))

    except:
      print 'INVALID DELETE EXCEPTION'
      return jsonify(status = 'INVALID', newurl = url_for('index'))

  print 'INVALID DELETE USER - BAD REQUEST'
  return jsonify(status = 'INVALID', newurl = url_for('index'))





# INVENTORY ROUTING ************************************************************

@app.route('/Inventory')
def inventory():
  """Load inventory page
  """
  #Steps:
  # if not logged in redirect to login
  # else display page

  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  #   NOTE!: I've added TEMP methods to allow for the page to function
  #   please, for the love of kittens everywhere, replace them with real
  #   code! D:

  #The User Object
  #user = TEMP_makeTestUser()#getUser(_WHAT_GOES_HURR??_)
  userLocs = inputGetUserLocations(user)[0]

  locsList = []  # Name, number of wines, list of wines 
  totalWineCount = 0
  totalRedCount = 0
  totalWhiteCount = 0
  totalLocCount = 0
  favoriteWines = []
  history = []
  favoriteAromas = []
  recommendedWines = []

  for loc in userLocs:
    totalLocCount += 1
    stat = inputViewStats(loc, user)[0]
    if type(stat) == str:
      continue

    
    locsList.append((loc.locationName.replace(chr(0xa0), ''), stat['wineCount'], stat['locWines']))

    totalWineCount += stat['wineCount']
    totalRedCount += stat['redCount']
    totalWhiteCount += stat['whiteCount']
    if stat['rating1'] != "None":
      favoriteWines.append(stat['rating1'])
    if stat['rating2'] != "None":
      favoriteWines.append(stat['rating2'])
    if stat['rating3'] != "None":
      favoriteWines.append(stat['rating3'])
    history += stat['history']
    favoriteAromas.append(stat['aroma1'])
    favoriteAromas.append(stat['aroma2'])
    favoriteAromas.append(stat['aroma3'])

  # Get top 3 favorite wines, recent history, and aromas
  favoriteWines.sort(key = lambda wine_rating: wine_rating[1], reverse = True)
  history.sort(key = lambda hist: hist.timestamp)
  favoriteAromas.sort(key = lambda aroma_val: aroma_val[1])

  count = 0
  favoriteWinesReal = []
  for wine in favoriteWines:
    if 2 < count:
      break
    favoriteWinesReal.append(wine[0])
    count += 1

  count = 0
  historyReal = []
  for hist in history:
    if 2 < count:
      break
    if hist.eventTag == 'add-wine':
      hist.eventTag = 'Added a new wine'
    elif hist.eventTag == 'move':
      hist.eventTag = 'Moved a wine to a different location'
    elif hist.eventTag == 'add-location':
      hist.eventTag = 'Added a new location'
    elif hist.eventTag == 'delete-wine':
      hist.eventTag = 'Deleted a wine'
    elif hist.eventTag == 'delete-inventory':
      hist.eventTag = 'Deleted an inventory'
    elif hist.eventTag == 'edit-location':
      hist.eventTag = 'Edited a location'
    elif hist.eventTag == 'edit-wine':
      hist.eventTag = 'Edited a wine\'s information'
    elif hist.eventTag == 'editEntryUser':
      hist.eventTag == 'Edited a wine\'s information'
    historyReal.append(hist)
    count += 1

  count = 0
  favoriteAromasReal = []
  for aroma in favoriteAromas:
    if 2 < count:
      break
    favoriteAromasReal.append(aroma[0])
    count += 1

  # Get recommendations
  shelf = inputGetUserShelves(user)[0]
  #if 0 < len(shelf):
    #shelf = shelf[0]
    #recommendations = inputRecommend(shelf.recommenderID, 3)[0]
  #else:
    #recommendations = []
  recommendations = []



  #A List of Wines from a User's Inventory (LocationInventory Objects)
  print 'About to load Wide Inventory'
  inventory = getWideInventory(user)
  print 'Successfully got back from the Wide Inventory DBAccess'
 
  #A List of Locations (Strings)
  locations = TEMP_makeLocationsListFromInventory(inventory[0])#getAllLocations(user)

  #A List of Wines from the Maind DB (Wine Objects)
  #wines = TEMP_makeFakeWineList(inventory)#???

  #A List of Filters (Strings)
  #print 'Making Type Filters'
  typeFilters = TEMP_makeTypeFiltersFromWines(inventory[0])#getAllWineTypes(user)
  #print 'Making Varietal Filters'
  varietalFilters = TEMP_makeVarietalFiltersFromWines(inventory[0])#getAllWineVarietals(user)
  #print 'Making Winery Filters'
  wineryFilters = TEMP_makeWineryFiltersFromWines(inventory[0])#getAllWineries(user)
  #print 'Making Vintage Filters'
  vintageFilters = TEMP_makeVintageFiltersFromWines(inventory[0])#getAllWineries(user)

  #A List of Tags (Strings)
  #print 'Making Tag List Filters'
  tagList = makeTagListFromWines(inventory[0])

  #Compile all of these lists into a fancy dictionary
  #print 'Making Filter Dictionary'
  filterDict = dict()
  filterDict['types'] = typeFilters
  filterDict['varietals'] = varietalFilters
  filterDict['wineries'] = wineryFilters
  filterDict['vintages'] = vintageFilters
  filterDict['tags'] = tagList

  #print 'Making USer Loc Objs'  
  fullLocations = inputGetUserLocations(user)
  for fl in fullLocations[0]:
    fl.locationName = fl.locationName.replace(chr(0xa0), '')

  #Render the template

  #print 'Rendering Inventory Template'
  return render_template('inventory_test.html', user = user, inventory = inventory[0], locations = locations, fullLocations = fullLocations[0], filters = filterDict, locsList = locsList, totalWineCount = totalWineCount, totalRedCount = totalRedCount, totalWhiteCount = totalWhiteCount, totalLocCount = totalLocCount, favoriteWines = favoriteWinesReal, favoriteAromas = favoriteAromasReal, recommendations = recommendations, history = historyReal)


@app.route('/Inventory/getWine')
def inventoryGetWine():
  """Get wine from user's inventory
  """

  #Steps:
  # if not logged in redirect to login
  # else display page
  #sid = request.cookies.get('wc_session_id')
  #user = getUserFromSession(sid)
  #if sid == None or user == None:
  #  return redirect(url_for('index'))
  
  print "Testing inventoryGetWine"
  locationID = 0
  wineID = 27
  user = UserInfo(userID=0)

  try:
    result = inputGetWine(locationID, wineID, user)
    print "yay inventoryGetWine got through"
    return result
    

  except:
    print "noooo something excepted"
    #return jsonify(status = 'INVALID')


@app.route('/Inventory/getLocation')
def inventoryGetLocation():
  """Get user's location
  """

  #Steps:
  # if not logged in redirect to login
  # else display page
  #sid = request.cookies.get('wc_session_id')
  #user = getUserFromSession(sid)
  #if sid == None or user == None:
  #  return redirect(url_for('index'))

  print "Testing inventoryGetLocation"
  locationID = 0
  user = UserInfo(userID=0)

  try:
    result = inputGetLocation(locationID, user) 
    print "yay inventoryGetLocation went through"
    return result 

  except:
    print "Oh nooo inventoryGetLocation failed"
    #return jsonify(status = 'INVALID')


@app.route('/Inventory/getLocationHistory')
def inventoryGetLocationHistory():
  """Get user's location history
  """

  #Steps:
  # if not logged in redirect to login
  # else display page
  #sid = request.cookies.get('wc_session_id')
  #user = getUserFromSession(sid)
  #if sid == None or user == None:
  #  return redirect(url_for('index'))

  print "Testing inventoryGetLocationHistory"
  locationID = 2
  wineID = 465
  user = UserInfo(userID=25)

  try:
    result = inputGetLocationHistory(locationID, wineID, user) 
    print "yay inventoryGetLocationHistory went through"
    return result 

  except:
    print "Oh nooo inventoryGetLocationHistory failed"
    #return jsonify(status = 'INVALID')

@app.route('/Inventory/getInventoryHistory')
def inventoryGetHistory():
  """ Get the location history for all locations in a user's inventory
      Sort them by timestamp with most recent first and return them
  """

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  history = []

  try:
    locations = inputGetUserLocations(user)
    if locations[0] == None:
      print "Error getting user locations"
    else:
      locations = locations[0]

    for loc in locations:
      locHistory = inputViewArchive(loc.locationID, user)
      if locHistory[0] == None:
        print "Error getting location history"
      else:
        locHistory = locHistory[0]
      for lhistory in locHistory:
        history.append(lhistory)

    # sort history by timestamp
    history.sort(key = lambda locHistory: locHistory.timestamp, reverse = True)

    print "History: " + str(history)
    print history[0].timestamp
    print history[1].timestamp
    print history[2].timestamp
    print history[3].timestamp
    return redirect(url_for('index'))


  except:
    print "Error in /Inventory/getInventoryHistory"
    ex, ex_type, tb = sys.exc_info()
    print ex
    print ex_type
    traceback.print_tb(tb)
    del tb

    return redirect(url_for('index'))


  


@app.route('/Inventory/getInventory')
def inventoryGetInventory():
  """Get user's inventory
  """

  #Steps:
  # if not logged in redirect to login
  # else display page
  #sid = request.cookies.get('wc_session_id')
  #user = getUserFromSession(sid)
  #if sid == None or user == None:
  #  return redirect(url_for('index'))

  print "Testing inventoryGetInventory"
  user = UserInfo(userID=25)

  try:
    result = inputGetInventory(user) 
    print "yay inventoryGetLocationHistory went through"
    return result 

  except:
    print "Oh nooo inventoryGetLocationHistory failed"
    #return jsonify(status = 'INVALID')


@app.route('/Inventory/searchInventory')
def inventorySearchInventory():
  """Search user's inventory for matching wine
  """

  #Steps:
  # if not logged in redirect to login
  # else display page
  #sid = request.cookies.get('wc_session_id')
  #user = getUserFromSession(sid)
  #if sid == None or user == None:
  #  return redirect(url_for('index'))

  #try:
    

  #except:
    #return jsonify(status = 'INVALID')


@app.route('/Inventory/addWine', methods=['POST'])
def inventoryAddWine():
  """Add wine to user's inventory
  """
  print '/Inventory/addWine - Now checking for Already Logged In'

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  print '/Inventory/addWine - Attempting to get Wine Fields'

  wine = dict()

  print '1'
  wine['wineName'] = sanitize(request.form['wineName'])
  print '2'
  print sanitize(request.form['wineLocation'])
  wine['wineLocation'] = int(sanitize(request.form['wineLocation']))#[0:sanitize(request.form['wineLocation']).find(' ')])
  print '3'
  wine['winery'] = sanitize(request.form['winery'])
  print '4'
  wine['region'] = sanitize(request.form['region'])
  print '5'
  wine['varietal'] = sanitize(request.form['varietal'])
  print '6'
  wine['vintage'] = sanitize(request.form['vintage'])
  print '7'

  #wine['imagePath'] = sanitize(request.form['wineImage']#Not A Path, needs image upload code
  try:
    wine['quantity'] = int(sanitize(request.form['quantity']))
  except:
    wine['quantity'] = 0
  print '8'
  try:
    wine['personalStarRating'] = int(sanitize(request.form['rating']))
  except:
    wine['personalStarRating'] = 3
  print '10'
  wine['tags'] = sanitize(request.form['quality'])
  print '11'
  wine['description'] = sanitize(request.form['description'])
  print '12'
  wine['isWishlist'] = False
  if 'wishList' in request.form:
    wine['isWishlist'] = True
  print '13'

  print "/Inventory/addWine - Made wine Dictionary"

  #ProfileImage
  validImage = False
  if request.files != None:
    myFile = request.files['wineImage']
    if myFile and allowed_file(myFile.filename):
      filename = binascii.b2a_hex(os.urandom(10)) + '.' + myFile.filename.rsplit('.', 1)[1]
      wine['imagePath'] = filename
      validImage = True

  print 'Image was valid'

  print 'Wine Quality form JSON: ' + str(wine['tags'])

  # Find varietal image if not valid image
  if validImage == False:
    if wine['varietal'] != None and wine['varietal'] != '':
      varietalImage = findVarietalMatch(wine['varietal']);
      varietalImage += '.jpg'
      wine['imagePath'] = varietalImage

  try:
    
    wineFloats = convertTagsToVector(wine['tags'])
    wine['bitter'] = wineFloats[0]
    wine['sweet'] = wineFloats[1]
    wine['sour'] = wineFloats[2]
    wine['salty'] = wineFloats[3]
    wine['chemical'] = wineFloats[4]
    wine['pungent'] = wineFloats[5]
    wine['oxidized'] = wineFloats[6]
    wine['microbiological'] = wineFloats[7]
    wine['floral'] = wineFloats[8]
    wine['spicy'] = wineFloats[9]
    wine['fruity'] = wineFloats[10]
    wine['vegetative'] = wineFloats[11]
    wine['nutty'] = wineFloats[12]
    wine['caramelized'] = wineFloats[13]
    wine['woody'] = wineFloats[14]
    wine['earthy'] = wineFloats[15]
    
    #Try to add a new wine
    addedWine = inputAddWineGlobal(wine)
    
    if addedWine[1] != None and addedWine[1][0] != None:
      for error in addedWine[1][0]:
        print 'Error: ' + error

    if addedWine[1] != None and addedWine[1][1] != None:
      for error in addedWine[1][1]:
        print 'SysError: ' + error

    wine['li_wineID'] = addedWine[0].wineID
    result = inputAddWineUser(wine, wine['quantity'], wine['wineLocation'], user)

    if result[1] != None and result[1][0] != None:
      for error in result[1][0]:
        print 'Error: ' + error

    if result[1] != None and result[1][1] != None:
      for error in result[1][1]:
        print 'SysError: ' + error


    print 'Wine has been added'

    if result[0] != None:#give this a condition

      if validImage:
        print 'Final File Path: ' + str(os.path.join(WINE_UPLOAD_FOLDER, filename))
        myFile.save(os.path.join(WINE_UPLOAD_FOLDER, filename))
      
      #Return json dictionary with a list of wines attached to a given key
      print 'Here comes JSON full of Dicts'
      return redirect(url_for('inventory'))
    else:
      print 'BAD DELETE VERIFICATION'
      return redirect(url_for('inventory'))

  except:
    ex, ex_type, tb = sys.exc_info()
    print ex
    print ex_type
    traceback.print_tb(tb)
    del tb
    print 'INVALID DELETE EXCEPTION'
    return redirect(url_for('inventory'))

  print 'INVALID DELETE USER - BAD REQUEST'
  return redirect(url_for('inventory'))




@app.route('/Inventory/verifAddWine', methods=['POST'])
def inventoryVerifAddWine():
  """Add wine to user's inventory
  """
  print '/Inventory/verifAddWine - Now checking for Already Logged In'

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  print '/Inventory/verifAddWine - Attempting to get Wine Fields'

  wine = dict()

  email = sanitize(request.form['email'])
  print '1'
  wine['wineName'] = sanitize(request.form['wineName'])
  print '2'
  wine['wineLocation'] = sanitize(request.form['wineLocation'])
  print '3'
  wine['winery'] = sanitize(request.form['winery'])
  print '4'
  wine['region'] = sanitize(request.form['region'])
  print '5'
  wine['varietal'] = sanitize(request.form['varietal'])
  print '6'
  wine['vintage'] = sanitize(request.form['vintage'])
  print '7'

  #wine['imagePath'] = sanitize(request.form['wineImage']#Not A Path, needs image upload code

  wine['quantity'] = sanitize(request.form['quantity'])
  print '8'
  wine['personalStarRating'] = sanitize(request.form['rating'])
  print '10'
  wine['tags'] = sanitize(request.form['quality'])
  print '11'
  wine['description'] = sanitize(request.form['description'])
  print '12'
  wine['isWishlist'] = sanitize(request.form['wishList'])
  print '13'

  print "/Inventory/addWine - Made wine Dictionary"

  if email == user.emailAddress:
    try:
      
      #Verify data?

      print 'Wine data has been verified'

      #Return json dictionary with a list of wines attached to a given key
      print 'Time to add the wine for reals'
      return jsonify(status = 'VALID')

    except:
      print 'INVALID DELETE EXCEPTION'
      return jsonify(status = 'INVALID')

  print 'INVALID DELETE USER - BAD REQUEST'
  return jsonify(status = 'INVALID')





@app.route('/Inventory/moveWine')
def inventoryMoveWine():
  """Move wine in user's inventory
  """

  #Steps:
  # if not logged in redirect to login
  # else display page
  #sid = request.cookies.get('wc_session_id')
  #user = getUserFromSession(sid)
  #if sid == None or user == None:
  #  return redirect(url_for('index'))

  #try:
    

  #except:
    #return jsonify(status = 'INVALID')


@app.route('/Inventory/addInventory', methods=['POST'])
def inventoryAddInventory():
  """Add a new inventory location
  """
  print '/Inventory/addInventory - Checking for login status'

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  print '/Inventory/addInventory - Grabbing values from POST'

  #make date
  date = str(datetime.datetime.now().replace(microsecond=0))

  dictLoc = dict()
  dictLoc['lm_userID'] = user.userID
  dictLoc['locationName'] = sanitize(request.form['addLocationName'])
  dictLoc['timeCreated'] = date

  print 'NOW WE GO FIND IMAGE K?'
  #IMAGE TIME GUYZ
  #ProfileImage
  validImage = False
  if request.files != None:
    myFile = request.files['addLocationImage']
    print 'File:' + str(myFile.filename)
    if myFile and allowed_file(myFile.filename):
      filename = binascii.b2a_hex(os.urandom(10)) + '.' + myFile.filename.rsplit('.', 1)[1]
      print filename
      dictLoc['imagePath'] = filename
      validImage = True

  print 'Image didn\'t cause a crash'

  try:
    result = inputAddInventory(user, dictLoc)


    if validImage:
      print 'Final File Path: ' + str(os.path.join(LOCATION_UPLOAD_FOLDER, filename))
      myFile.save(os.path.join(LOCATION_UPLOAD_FOLDER, filename))



    print "Yay add inventory got through"
    
    return redirect(url_for('inventory'))

  except:
    print "Exception occured in inputAddInventory"
    ex, ex_type, tb = sys.exc_info()
    print ex
    print ex_type
    traceback.print_tb(tb)
    del tb
    return redirect(url_for('inventory'))
    #return jsonify(status = 'INVALID')
  return redirect(url_for('inventory'))



@app.route('/Inventory/deleteWine', methods=['POST'])
def inventoryDeleteWine():
  """Delete wine from inventory
  """
  print '/Inventory/deleteWine - Running test'

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  wineID = int(sanitize(request.form['li_wineID']))
  locationID = int(sanitize(request.form['li_locationID'].replace('loc_','')))

  print "So this is what we got"

  print "Deleting"
  try:
    result = inputDeleteWineUser(user, wineID, locationID)
    print "Yay delete wine got through"
    print result
    return jsonify(status = 'VALID')

  except:
    print "Exception occured in inputDeleteWineUser"
    return jsonify(status = 'INVALID')


@app.route('/Inventory/deleteInventory', methods=['POST'])
def inventoryDeleteInventory():
  """Delete user's inventory location
  """

  #Steps:
  # if not logged in redirect to login
  # else display page
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  locationID = int(sanitize(request.form['locationID'].replace('loc_','')))
  print "Deleting location" + str(locationID)

  try:
    result = inputDeleteInventory(locationID, user)
    print "Delete worked"
    
    return jsonify(status = 'VALID')

  except:
    print "Exception in delete"
    return jsonify(status = 'INVALID')


@app.route('/Inventory/editInventory', methods=['POST'])
def inventoryEditInventory():
  """Edit user's inventory location
  """
  print "In editInventory"
  #Steps:
  # if not logged in redirect to login
  # else display page
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  print "Getting location number"
  locationID = int(sanitize(request.form['editLocationNumber'].replace('loc_','')))
  print locationID

  print "Getting location name"
  nameChange = sanitize(request.form['editLocationName'])
  print "Things gotten"

  changes = {}

  # Check image file
  validImage = False
  if request.files != None:
    print "Getting Location Image"
    myFile = request.files['editLocationImage']
    print 'File:' + str(myFile.filename)
    if myFile and allowed_file(myFile.filename):
      filename = binascii.b2a_hex(os.urandom(10)) + '.' + myFile.filename.rsplit('.', 1)[1]
      print filename
      validImage = True
      changes['imagePath'] = filename

  if nameChange != '':
    changes['locationName'] = nameChange

  try:
    result = inputEditInventory(locationID, changes, user)

    if result[1] != None and result[1][0] != None:
      for error in result[1][0]:
        print 'Error: ' + error

    if result[1] != None and result[1][1] != None:
      for error in result[1][1]:
        print 'SysError: ' + error

    if validImage:
      print str(os.path.join(LOCATION_UPLOAD_FOLDER, filename))
      myFile.save(os.path.join(LOCATION_UPLOAD_FOLDER, filename))
    
    return redirect(url_for('inventory'))

  except:
    print "Exception occured in inventoryEditInventory"
    return redirect(url_for('inventory'))

  return redirect(url_for('inventory'))



@app.route('/Inventory/editEntry', methods=['POST'])
def inventoryEditEntry():
  """Edit user's wine
  """

  #Steps:
  # if not logged in redirect to login
  # else display page
  #sid = request.cookies.get('wc_session_id')
  #user = getUserFromSession(sid)
  #if sid == None or user == None:
  #  return redirect(url_for('index'))


  print '/Inventory/editEntry - Now checking for Already Logged In'

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  print '/Inventory/editEntry - Attempting to get Wine Fields'

  wine = dict()

  #ONLY ADD THINGS TO THE MAP IF THEY ARE NOT EMPTY
  print '1'
  if len(sanitize(request.form['edit_wineID'])) > 0:
    wine['wineID'] = sanitize(request.form['edit_wineID'])
  print '2'
  if len(sanitize(request.form['edit_wineName'])) > 0:
    wine['wineName'] = sanitize(request.form['edit_wineName'])
  print '3'
  print sanitize(request.form['edit_wineLocation'])
  if len(sanitize(request.form['edit_wineLocation'])) > 0:
    wine['li_locationID'] = int(sanitize(request.form['edit_wineLocation'].replace('loc_','')))#[0:sanitize(request.form['edit_wineLocation']).find(' ')])
    print sanitize(request.form['edit_wineLocation'])

  if len(sanitize(request.form['original_wineLocation'])) > 0:
    wine['original_wineLocation'] = int(sanitize(request.form['original_wineLocation']))

  print '4'
  if len(sanitize(request.form['edit_winery'])) > 0:
    wine['winery'] = sanitize(request.form['edit_winery'])
  print '5'
  if len(sanitize(request.form['edit_region'])) > 0:
    wine['region'] = sanitize(request.form['edit_region'])
  print '6'
  if len(sanitize(request.form['edit_varietal'])) > 0:
    wine['varietal'] = sanitize(request.form['edit_varietal'])
  print '7'
  if len(sanitize(request.form['edit_vintage'])) > 0:
    wine['vintage'] = sanitize(request.form['edit_vintage'])
  print '8'
  if sanitize(request.form['edit_quantity']) != 'None' and len(sanitize(request.form['edit_quantity'])) > 0:
    wine['quantity'] = int(sanitize(request.form['edit_quantity']))
  print '9'
  if sanitize(request.form['edit_personalStarRating']) != 'None' and len(sanitize(request.form['edit_personalStarRating'])) > 0:
    wine['personalStarRating'] = int(sanitize(request.form['edit_personalStarRating']))
  print '10'
  if len(sanitize(request.form['edit_quality'])) > 0:
    wine['tags'] = sanitize(request.form['edit_quality'])
  else:
    wine['tags'] = ''
  print '11'
  if len(sanitize(request.form['edit_description'])) > 0:
    wine['description'] = sanitize(request.form['edit_description'])
  print '12'
  wine['isWishlist'] = False
  if 'wishList' in request.form:
    wine['isWishlist'] = True

  print "/Inventory/editEntry - Made wine Dictionary"

  #ProfileImage
  validImage = False
  if request.files != None:
    myFile = request.files['edit_wineImage']
    print 'File:' + str(myFile.filename)
    if myFile and allowed_file(myFile.filename):
      filename = binascii.b2a_hex(os.urandom(10)) + '.' + myFile.filename.rsplit('.', 1)[1]
      print filename
      wine['imagePath'] = filename
      validImage = True

  print 'Image was valid'

  print 'Wine Quality form JSON: ' + str(wine['tags'])


  try:
    
    wineFloats = convertTagsToVector(wine['tags'])
    wine['bitter'] = wineFloats[0]
    wine['sweet'] = wineFloats[1]
    wine['sour'] = wineFloats[2]
    wine['salty'] = wineFloats[3]
    wine['chemical'] = wineFloats[4]
    wine['pungent'] = wineFloats[5]
    wine['oxidized'] = wineFloats[6]
    wine['microbiological'] = wineFloats[7]
    wine['floral'] = wineFloats[8]
    wine['spicy'] = wineFloats[9]
    wine['fruity'] = wineFloats[10]
    wine['vegetative'] = wineFloats[11]
    wine['nutty'] = wineFloats[12]
    wine['caramelized'] = wineFloats[13]
    wine['woody'] = wineFloats[14]
    wine['earthy'] = wineFloats[15]
    
    #Try to add a new wine
    editedWine = inputEditWineGlobal(wine) 
    print "yay inventoryEditEntry went through"
    
    if editedWine[1] != None and editedWine[1][0] != None:
      for error in editedWine[1][0]:
        print 'Error: ' + error

    if editedWine[1] != None and editedWine[1][1] != None:
      for error in editedWine[1][1]:
        print 'SysError: ' + error

    wine['li_wineID'] = editedWine[0].wineID
    result = inputEditEntryUser(int(wine['original_wineLocation']), int(wine['wineID']), wine, user)

    if result[1] != None and result[1][0] != None:
      for error in result[1][0]:
        print 'Error: ' + error

    if result[1] != None and result[1][1] != None:
      for error in result[1][1]:
        print 'SysError: ' + error


    print 'Wine has been edited'

    if result[0] != None:#give this a condition

      if validImage:
        print 'Final File Path: ' + str(os.path.join(WINE_UPLOAD_FOLDER, filename))
        myFile.save(os.path.join(WINE_UPLOAD_FOLDER, filename))
      
      #Return json dictionary with a list of wines attached to a given key
      print 'Here comes JSON full of Dicts'
      return redirect(url_for('inventory'))
    else:
      print 'BAD DELETE VERIFICATION'
      return redirect(url_for('inventory'))

  except:
    ex, ex_type, tb = sys.exc_info()
    print ex
    print ex_type
    traceback.print_tb(tb)
    del tb
    print 'INVALID DELETE EXCEPTION'
    return redirect(url_for('inventory'))

  print 'INVALID DELETE USER - BAD REQUEST'
  return redirect(url_for('inventory'))


  print "Testing inventoryEditEntry"
  locationID = 2
  wineID = 465
  user = UserInfo(userID=25)
  changes = {'description':'hella'}

  try:
    result = inputEditEntryUser(locationID, wineID, changes, user) 
    print "yay inventoryEditEntry went through"
    return result 

  except:
    print "Oh nooo inventoryEditEntry failed"
    #return jsonify(status = 'INVALID')


@app.route('/Inventory/importInventory')
def inventoryImportInventory():
  """Import user's inventory
  """

  #Steps:
  # if not logged in redirect to login
  # else display page
  #sid = request.cookies.get('wc_session_id')
  #user = getUserFromSession(sid)
  #if sid == None or user == None:
  #  return redirect(url_for('index'))

  #try:
    

  #except:
    #return jsonify(status = 'INVALID')


@app.route('/Inventory/exportInventory')
def inventoryExportInventory():
  """Export user's inventory
  """

  #Steps:
  # if not logged in redirect to login
  # else display page
  #sid = request.cookies.get('wc_session_id')
  #user = getUserFromSession(sid)
  #if sid == None or user == None:
  #  return redirect(url_for('index'))

  #try:
    

  #except:
    #return jsonify(status = 'INVALID')


@app.route('/Inventory/viewStats')
def inventoryViewStats():
  """View stats about an inventory
  """

  #Steps:
  # if not logged in redirect to login
  # else display page
  #sid = request.cookies.get('wc_session_id')
  #user = getUserFromSession(sid)
  #if sid == None or user == None:
  #  return redirect(url_for('index'))

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  print "Beginning view stats test"

  try:

    locations = inputGetUserLocations(user)

    if locations[0] == None:
      print "Error getting user locations"
    else:
      locations = locations[0]

    for loc in locations:
      if loc == None:
        continue

      stats = inputViewStats(loc,user)
      if stats[0] == None:
        print 'Error getting statistics'
      else:
        stats = stats[0]
      print "STAT: " + str(stats)

    return redirect(url_for('index'))

  except:
    print "Exception in view stats"
    view_traceback()
    return redirect(url_for('index'))




@app.route('/Inventory/sortInventory')
def inventorySortInventory():
  """Sort user's inventory
  """

  #Steps:
  # if not logged in redirect to login
  # else display page
  #sid = request.cookies.get('wc_session_id')
  #user = getUserFromSession(sid)
  #if sid == None or user == None:
  #  return redirect(url_for('index'))

  #try:
    

  #except:
    #return jsonify(status = 'INVALID')


@app.route('/Inventory/viewArchive')
def inventoryViewArchive():
  """View archive of user's inventory location
  """

  #Steps:
  # if not logged in redirect to login
  # else display page
  #sid = request.cookies.get('wc_session_id')
  #user = getUserFromSession(sid)
  #if sid == None or user == None:
  #  return redirect(url_for('index'))

  #try:
    

  #except:
    #return jsonify(status = 'INVALID')


@app.route('/Inventory/rateWine')
def inventoryRateWine():
  """Rate user's wine
  """

  #Steps:
  # if not logged in redirect to login
  # else display page
  #sid = request.cookies.get('wc_session_id')
  #user = getUserFromSession(sid)
  #if sid == None or user == None:
  #  return redirect(url_for('index'))

  #try:
    

  #except:
    #return jsonify(status = 'INVALID')


# RECOMMENDER ROUTING **********************************************************

@app.route('/Recommend')
def recommend():
  """Load Recommendations page
  """
  #Steps:
  # if not logged in redirect to login
  # else display page

  #get from cookies
  sid = request.cookies.get('wc_session_id')

  #get the user object if it exists
  user = getUserFromSession(sid)

  #if user is None we need to redirect to login page
  if user == None:
    return redirect(url_for('index'))


  userLocs = inputGetUserLocations(user)[0]

  locsList = []  # Name, number of wines, list of wines 
  totalWineCount = 0
  totalRedCount = 0
  totalWhiteCount = 0
  totalLocCount = 0
  favoriteWines = []
  history = []
  favoriteAromas = []
  recommendedWines = []

  for loc in userLocs:
    totalLocCount += 1
    stat = inputViewStats(loc, user)[0]
    if type(stat) == str:
      continue

    
    locsList.append((loc.locationName.replace(chr(0xa0), ''), stat['wineCount'], stat['locWines']))

    totalWineCount += stat['wineCount']
    totalRedCount += stat['redCount']
    totalWhiteCount += stat['whiteCount']
    if stat['rating1'] != "None":
      favoriteWines.append(stat['rating1'])
    if stat['rating2'] != "None":
      favoriteWines.append(stat['rating2'])
    if stat['rating3'] != "None":
      favoriteWines.append(stat['rating3'])
    history += stat['history']
    favoriteAromas.append(stat['aroma1'])
    favoriteAromas.append(stat['aroma2'])
    favoriteAromas.append(stat['aroma3'])

  # Get top 3 favorite wines, recent history, and aromas
  favoriteWines.sort(key = lambda wine_rating: wine_rating[1], reverse = True)
  history.sort(key = lambda hist: hist.timestamp)
  favoriteAromas.sort(key = lambda aroma_val: aroma_val[1])

  count = 0
  favoriteWinesReal = []
  for wine in favoriteWines:
    if 2 < count:
      break
    favoriteWinesReal.append(wine[0])
    count += 1

  count = 0
  historyReal = []
  for hist in history:
    if 2 < count:
      break
    if hist.eventTag == 'add-wine':
      hist.eventTag = 'Added a new wine'
    elif hist.eventTag == 'move':
      hist.eventTag = 'Moved a wine to a different location'
    elif hist.eventTag == 'add-location':
      hist.eventTag = 'Added a new location'
    elif hist.eventTag == 'delete-wine':
      hist.eventTag = 'Deleted a wine'
    elif hist.eventTag == 'delete-inventory':
      hist.eventTag = 'Deleted an inventory'
    elif hist.eventTag == 'edit-location':
      hist.eventTag = 'Edited a location'
    elif hist.eventTag == 'edit-wine':
      hist.eventTag = 'Edited a wine\'s information'
    elif hist.eventTag == 'editEntryUser':
      hist.eventTag == 'Edited a wine\'s information'
    historyReal.append(hist)
    count += 1

  count = 0
  favoriteAromasReal = []
  for aroma in favoriteAromas:
    if 2 < count:
      break
    favoriteAromasReal.append(aroma[0])
    count += 1

  # Get recommendations
  shelf = inputGetUserShelves(user)[0]
  #if 0 < len(shelf):
    #shelf = shelf[0]
    #recommendations = inputRecommend(shelf.recommenderID, 3)[0]
  #else:
    #recommendations = []
  recommendations = []



  fullShelves = inputGetUserShelves(user)[0]
  fullLocations = inputGetUserLocations(user)[0]
  for fl in fullLocations:
    fl.locationName = fl.locationName.replace(chr(0xa0), '')

  fullRecommended = {}

  for shelf in fullShelves:
    recommended = inputGetRecommendHistory(shelf.recommenderID)
    if recommended[0] != None:
      recommended = recommended[0]
    else:
      continue
    if len(recommended) < 3:
      more = inputRecommend(shelf.recommenderID,3 - len(recommended))
      if more[0]  != None:
        recommended.extend(more[0])
      #print "RECOMMENDED: " + str(recommended)
    fullRecommended[shelf.recommenderID] = recommended


  #Render Template
  return render_template('recommender.html', fullRecommended = fullRecommended, fullShelves = fullShelves, fullLocations = fullLocations, user = user, locsList = locsList, totalWineCount = totalWineCount, totalRedCount = totalRedCount, totalWhiteCount = totalWhiteCount, totalLocCount = totalLocCount, favoriteWines = favoriteWinesReal, favoriteAromas = favoriteAromasReal, recommendations = recommendations, history = historyReal)

@app.route('/Recommend/getRecommendations', methods=['POST'])
def getRecommended():
  """ Get more recommended wines for the user
  """
  #Steps:
  # if not logged in redirect to login
  # else display page

  #get from cookies
  print "Before sid in recommend route"
  sid = request.cookies.get('wc_session_id')

  #get the user object if it exists
  user = getUserFromSession(sid)

  print "In recommend route"
  #if user is None we need to redirect to login page
  if user == None:
    return redirect(url_for('index'))

  recommenderID = int(sanitize(request.form['recommenderID']))

  print "Getting more recommendations"  
  recommended = inputRecommend(recommenderID, 3)
  print "Recommendations received"
  #print recommended
  if recommended[0] == None:
    return jsonify(status = 'INVALID')
  recommended = recommended[0]

  dictList = list()
  for item in recommended:
    try:
      dictList.append(item.__dict__)
    except:
      return jsonify(status = 'INVALID')

  #print dictList
  return jsonify(status = 'VALID', candidates = dictList)



@app.route('/Recommend/candidateWines', methods=['POST'])
def candidateWines():
  """Load Recommendations page
  """

  print '/Recommend/candidateWines - Now checking for Already Logged In'

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  print '/Recomend/candidateWines - Attempting to Get Candidate Wines'

  attrs = dict()
  attrs['wineName'] = sanitize(request.form['wineName']).replace('\'', '')
  attrs['winery'] = sanitize(request.form['winery']).replace('\'', '')
  attrs['vintage'] = sanitize(request.form['vintage']).replace('\'', '')

  print "/Recommend/candidateWines - Made attribute Dictionary"

  try:
    
    #Get candidate list from DB
    candidateWines = inputGetCandidateWines(attrs)

    print 'YAY!! WE R GOT WINEZ LOL'

    #print str(candidateWines)
    dictList = list()
    for i in range(0, len(candidateWines[0])):
      wine = candidateWines[0][i]
      dictList.append(wine.__dict__)


    if len(candidateWines) > 0:
      
      #Return json dictionary with a list of wines attached to a given key
      print 'Here comes JSON full of Dicts'
      return jsonify(status = 'VALID', candidates = dictList)
    else:
      print 'BAD DELETE VERIFICATION'
      return jsonify(status = 'INVALID')

  except:
    print 'INVALID DELETE EXCEPTION'
    return jsonify(status = 'INVALID')

  print 'INVALID DELETE USER - BAD REQUEST'
  return jsonify(status = 'INVALID')



@app.route('/Recommend/createShelf', methods=['POST'])
def createShelf():
  """Load Recommendations page
  """

  print '/Recommend/createShelf - Now checking for Already Logged In'

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  print '/Recomend/createShelf - Attempting to get Seed Wine List'

  attrs = dict()

  email = sanitize(request.form['email'])
  attrs['shelfName'] = sanitize(request.form['shelfName'])
  attrs['seeds'] = json.loads(request.form['seeds'])

  print "/Recommend/createShelf - Made attribute Dictionary"

  print 'Seed Attribute form JSON: ' + str(attrs['seeds'])

  intSeeds = list()
  for wineID in attrs['seeds']:
    intSeeds.append(int(wineID))
    print 'Seed WineID:' + str(wineID)


  if email == user.emailAddress:
    try:
      
      #Try to create a new shelf
      channel = inputCreateChannel(user, str(attrs['shelfName']), intSeeds)

      if channel[1] != None and channel[1][0] != None:
        for error in channel[1][0]:
          print 'Error: ' + error

      if channel[1] != None and channel[1][1] != None:
        for error in channel[1][1]:
          print 'SysError: ' + error

      print 'Shelf has been created'


      if True:#give this a condition
        
        #Return json dictionary with a list of wines attached to a given key
        print 'Here comes JSON full of Dicts'
        return jsonify(status = 'VALID')
      else:
        print 'BAD DELETE VERIFICATION'
        return jsonify(status = 'INVALID')

    except:
      print 'INVALID DELETE EXCEPTION'
      return jsonify(status = 'INVALID')

  print 'INVALID DELETE USER - BAD REQUEST'
  return jsonify(status = 'INVALID')

@app.route('/Recommend/editShelf', methods=['POST'])
def editShelf():
  """Load Recommendations page
  """

  print '/Recommend/editShelf - Now checking for Already Logged In'

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  print '/Recommend/editShelf - Attempting to get Seed Wine List'

  attrs = dict()

  # Do we need these two for edit Shelf?
  email = sanitize(request.form['email'])
  print '1'
  #attrs['shelfName'] = sanitize(request.form['shelfName']

  attrs['recommenderID'] = sanitize(request.form['recommenderID'])
  print '2'
  attrs['seeds'] = json.loads(request.form['seeds'])
  print '3'
  #attrs['name'] = sanitize(request.form['channelName']

  print "/Recommend/editShelf - Made attribute Dictionary"

  print 'Seed Attribute form JSON: ' + str(attrs['seeds'])

  intSeeds = list()
  for wineID in attrs['seeds']:
    intSeeds.append(int(wineID))
    print 'Seed WineID:' + wineID


  if email == user.emailAddress:
    try:

      #Get all the seeds from the current shelf
      recommenderID = int(attrs['recommenderID'])
      currSeeds = inputGetSeeds(recommenderID)

      if currSeeds[1] != None and currSeeds[1][0] != None:
        for error in currSeeds[1][0]:
          print 'Error: ' + error
          
      if currSeeds[1] != None and currSeeds[1][1] != None:
        for error in currSeeds[1][1]:
          print 'Error: ' + error

      print 'Seeds have been obtained'

      # Try to remove the seeds from the shelf
      seedIDs = []

      for seed in currSeeds[0]:
        print seed
        print seed.wineID
        seedIDs.append(seed.wineID)

      if len(seedIDs) != 0:
        removed = inputRemoveSeeds(recommenderID,seedIDs)

        if removed[1] != None and removed[1][0] != None:
          for error in removed[1][0]:
            print 'Error: ' + error
            
        if removed[1] != None and removed[1][1] != None:
          for error in removed[1][0]:
            print 'Error: ' + error
        print 'Seeds have been removed'
      else:
        print "seedIDs: " + str(seedIDs)

 
      print "Adding with intSeeds: " + str(intSeeds)
      # Add all the new seeds the user specified
      added = inputAddSeeds(recommenderID, intSeeds)

      if added[1] != None and added[1][0] != None:
        for error in added[1][0]:
          print 'Error: ' + error
          
      if added[1] != None and added[1][1] != None:
        for error in added[1][0]:
          print 'Error: ' + error


      # Change channel name
      #nameChange = inputEditChannel(recommenderID, attrs['name'])
      #if nameChange[0] == None:
        #print 'Error in name change' 

      print 'Seeds have been added'

      if True:#give this a condition
        # Is this the right stuff to be done here?        
        print 'Here comes JSON full of Dicts'
        return jsonify(status = 'VALID')
      else:
        print 'BAD DELETE VERIFICATION'
        return jsonify(status = 'INVALID')

    except:
      print 'INVALID DELETE EXCEPTION'
      ex, ex_type, tb = sys.exc_info()
      print ex
      print ex_type
      traceback.print_tb(tb)
      del tb
      return jsonify(status = 'INVALID')

  print 'INVALID DELETE USER - BAD REQUEST'
  return jsonify(status = 'INVALID')

@app.route('/Recommend/addFromRecommendToInventory', methods=['POST'])
def addFromRecommendToInventory():
  """ Adds a wine by it's id to a location in that user's inventory that they specify """

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  attrs = dict()

  try:
    attrs['wineID'] = sanitize(request.form['wineID'])
    attrs['locationID'] = sanitize(request.form['locationID'].replace('loc_',''))
    #attrs['count'] = sanitize(request.form['count']


    added = inputAddWineUserByID(int(attrs['wineID']),1,int(attrs['locationID']),user)

    #TEMP return
    return jsonify(status = 'VALID')


  except:
    print "Error in addFromRecommendToInventory"
    view_traceback()
    # TEMP return
    return jsonify(status = 'INVALID')

@app.route('/Recommend/getSeeds', methods=['POST'])
def getSeeds():
  """Load Recommendations page
  """

  print '/Recommend/getSeeds - Now checking for Already Logged In'

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  print '/Recommend/getSeeds - Attempting to Get Seeds'

  attrs = dict()
  attrs['recID'] = sanitize(request.form['recID'])

  print "/Recommend/getSeeds - Made attribute Dictionary"
    
  #Get candidate list from DB
  seeds = inputGetSeeds(int(attrs['recID']))

  dictList = list()
  for i in range(0, len(seeds[0])):
    wine = seeds[0][i]
    dictList.append(wine.__dict__)

  print 'YAY!! WE R GOT WINEZ SEEDZ LOL'

  return jsonify(seedList = dictList)

@app.route('/Recommend/delete', methods=['POST'])
def deleteShelf():

  print '/Recommend/delete - Now checking for Already Logged In'

  #If the user is already logged in then redirect them to their profile
  sid = request.cookies.get('wc_session_id')
  user = getUserFromSession(sid)
  if sid == None or user == None:
    return redirect(url_for('index'))

  print '/Recommend/delete - Attempting to Delete Shelf'

  attrs = dict()
  attrs['recID'] = sanitize(request.form['recID'])

  print "/Recommend/delete - Made attribute Dictionary"

  email = sanitize(request.form['email'])

  if email == user.emailAddress:
    try:
      deletedShelf = inputRemoveChannel(int(attrs['recID']))
      if deletedShelf[0] != None:
        return jsonify(status = 'VALID')
      else:
        print 'BAD DELETE VERIFICATION'
        return jsonify(status = 'INVALID')

    except:
      print 'INVALID DELETE EXCEPTION'
      view_traceback()
      return jsonify(status = 'INVALID')

  print 'INVALID DELETE USER - BAD REQUEST'
  return jsonify(status = 'INVALID')




# UTILITY METHODS **************************************************************

def sanitize(str):
  return str.replace('\'','').replace('\"','').replace('<', '').replace('>', '').replace('\n', '').replace('\r', '').replace('script', '')

def getUserFromSession(sid):
  if sid == None:
    return None
  try:
    return sessions[sid]
  except KeyError:
    return None


def allowed_file(filename):
  if len(filename) < 5:
    return False
  return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def view_traceback():
    ex, ex_type, tb = sys.exc_info()
    print ex
    print ex_type
    traceback.print_tb(tb)
    del tb