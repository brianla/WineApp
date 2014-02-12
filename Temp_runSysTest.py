from flask import *
from Classes import *
from InstantiationValidation import *
from InventoryIOController import *
from UserIOController import *
from collections import OrderedDict
import random
import sys
import traceback
from datetime import datetime
from Temp_runRecTest import *

DEBUG = True

#global logging list
log = list()

app = Flask(__name__)

thisUser = None 

@app.route('/')
def index():
  """Output Console
  """
  log = list()

  resp = make_response(render_template('unit_test_console.html', log = log))

  try:
    TEMP_testLogin(log)
    #runLoginTests(log)
    # runInventoryTests(log,thisUser)
    #runClusters(log)
    runRecTests(log,thisUser)
  except:
    view_traceback()
    exit(0)
  #print "Here"
  resp = make_response(render_template('unit_test_console.html', log = log))
  resp.set_cookie('username',25)
  return resp

def runClusters(log):
  dbSetClusterID(6,600)
  dbSetCSOByWineID(6,True)
  log.append("Trying to update the clusters...")
  try:
    print "Just before clustering"
    log.append(str(updateClusters()))
    print "Ran the clustering"
  except:
    view_traceback()
  log.append("Updated the clusters.")

def view_traceback():
	ex_type,ex,tb = sys.exc_info()
	#print ex_type
	#print ex
	#print traceback.print_tb(tb)
	del tb

def runInventoryTests(log,thisUser):
	"""
	#################################
	#     Testing Invalid Input     #
	#################################
	# Login

	#print "\tGetting a BAD wine..."
	# Correct output 4:24pm 5/28/13 SH
	log.append("Getting a BAD wine...")
	try:
		TEMP_testInputGetWineBad(log)
	except:
		view_traceback()
		exit(0)
	#print "\tGetting a BAD location..."
	# Correct output 4:25pm 05/28/13 SH
	log.append("Getting BAD location...")
	try:
		TEMP_testInputGetLocationBad(log)
	except:
		view_traceback()
		exit(0)	


	# TODO need to login with different user with no locations
	#log.append("Getting BAD locations...")	

	# TODO check invalid location history fetching

	# TODO need to login with different user with no wines
	#log.append("Getting bad inventory...")


	#print "\tAdding wine BAD..."
	# Correct Output 4:26pm 05/28/13 SH
	log.append("Adding wine BAD...")
	try:
		TEMP_testInputAddWineUserBad(log)
	except:
		view_traceback()
		exit(0)	
		
	# Correct output 4:27 pm 05/28/13 SH
	log.append("Moving wine BAD...")
	try:
		TEMP_testInputMoveWineBad(log)
	except:
		view_traceback()
		exit(0)	

	# Correct output 4:29pm 05/28/13 SH
	log.append("Adding inventory BAD...")
	try:
		TEMP_testInputAddInventoryBad(log)
	except:
		view_traceback()
		exit(0)	
		
	# Correct Output 6:39pm 05/28/13 SH
	log.append("Deleting wines in inventory BAD...")
	try:
		if DEBUG:
			print "testing deleting a wine"
		TEMP_testInputDeleteWineUserBad(log)
	except:
		view_traceback()
		exit(0)	

	# Correct Output 4:35 pm 05/28/13
	log.append("Deleting inventory BAD...")
	try:
		TEMP_testInputDeleteInventoryBad(log)
	except:
		view_traceback()
		exit(0)	
		
		
	log.append("Editing inventory BAD...")
	try:
		TEMP_testInputEditInventoryBad(log)
	except:
		view_traceback()
		exit(0)	
		
		
	log.append("Editing wine entries BAD...")
	try:
		TEMP_testInputEditEntryUserBad(log)
	except:
		view_traceback()
		exit(0)	
		
		
	log.append("Viewing archive BAD...")
	try:
		TEMP_testInputViewArchiveBad(log)
	except:
		view_traceback()
		exit(0)	
	
	
	log.append("Rating wine BAD...")
	try:
		TEMP_testRateWineUserBad(log)
	except:
		view_traceback()
		exit(0)	


	#################################
	#      Testing Valid Input      #
	#################################

	# Make a wine location
	#log.append("Making a location...")
	#TEMP_testInputAddInventory(log)

 	# Correct Output 4:35pm 05/28/13 SH	
	log.append("Getting a wine...")
	TEMP_testInputGetWine(log)

	# Correct Output 4:35pm 05/28/13 SH
	log.append("Getting a location...")
	TEMP_testInputGetLocation(log)
     	""" 

	# Correct Output 4:35pm 05/28/13 SH
	log.append("Getting all the user's locations...")
	TEMP_testInputGetUserLocations(log)


	# FIX: Not yet implemented in data access 6:45 pm 05/28/13 SH
	log.append("Getting a location history...")	
	TEMP_testInputGetLocationHistory(log)

	log.append("Getting a global wine...")
	TEMP_testInputGetWineGlobal(log)

	"""
	# Correct Output 4:35pm 05/28/13 SH
        log.append("Getting this user's inventory...")
	TEMP_testInputGetInventory(log,thisUser)

	# FIX	
	#Partially correct 4:35pm 05/28/13
	# I think it allows the user to add as many instances of the same
	# wine as they want without incrementing the count
	# DB team is on it 6:53pm SH
	log.append("Testing adding a wine...")
	TEMP_testInputAddWineUser(log)

	# Correct Output 4:35pm 05/28/13 SH
	log.append("Testing adding an inventory...")
	TEMP_testInputAddInventory(log)
	"""

	# FIX	
	log.append("Testing moving a wine...")
	TEMP_testInputMoveWine(log)


	"""
	# Correct Output
	# 9:10 pm 05/28/13 SH
	log.append("Testing deleting a wine...")
	TEMP_testInputDeleteWineUser(log)

	# Correct Output 4:35pm 05/28/13 SH
	log.append("Testing deleting an inventory...")
	TEMP_testInputDeleteInventory(log)

	# Correct Output 4:35pm 05/28/13 SH
	log.append("Testing editing an inventory...")
	TEMP_testInputEditInventory(log)

	# Correct Output 4:35pm 05/28/13 SH
	log.append("Testing editng a wine...")
	TEMP_testInputEditEntryUser(log)
	"""


	#print "\tTesting import, export, stats and archive..."
	TEMP_testImportInventory(log)
	TEMP_testExportInventory(log)
	TEMP_testInputViewStats(log)

	"""
	# Correct Output 4:35pm 05/28/13 SH
	TEMP_testInputViewArchive(log)
	
	# Correct Output 4:35pm 05/28/13 SH
	log.append("Testing rating a wine...")
	TEMP_testInputRateWineUser(log)
	"""

def runLoginTests(log):
	#################################
	#     Testing Invalid Input     #
	#################################
  	#temp_testadduser(log)

	log.append("Using session id: " + str(request.cookies.get('username')) )
	log.append(" Testing add user...")
	try:
		TEMP_testAddUserBad(log)
	except:
		log.append('TEMP_testAddUserBad(log) failed with exception: ' + sys.exc_info()[0])

	log.append(" Testing Login...")
	try:
		TEMP_testLoginBad(log)
	except:
		log.append('TEMP_testLoginBad(log) failed with exception: ' + sys.exc_info()[0])

	log.append(" Testing Logout...")
	try:
		TEMP_testLogoutBad(log)
	except:
		log.append('TEMP_testLogoutBad(log) failed with exception: ' + sys.exc_info()[0])

	log.append(" Test editing a user...")
	# Can't do without a session
	try:
                TEMP_testEditUserBad(log)
        except:
                log.append('TEMP_testEditUserBad(log) failed with exception: ' + sys.exc_info()[0])

	#################################
	#      Testing Valid Input      #
	#################################
	log.append("Testing a valid login")
	try:
		TEMP_testLogin(log)
	except:
		log.append('TEMP_testLogin(log) failed with exception: ' + sys.exc_info()[0])


	log.append("Testing a valid edit")
	try:
		TEMP_testEditUser(log)
	except:
		log.append('TEMP_testEditUser(log) failed with exception: ' + sys.exc_info()[0])


##############################################################################
#    Start General Inv Test Code
##############################################################################


################ Tests for invalid input ######################

def TEMP_testAddUserBad(log):
	#### Email Tests ####
        emailNone = {
	            'emailAddress':None,
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputCreateUser(emailNone)
	log.append("For emailAddress = None: " + str(result))

        noEmail = {
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputCreateUser(noEmail)
	log.append("For no email in the dict: " + str(result))

        invalidEmail = {
	            'emailAddress': "Nyan cat needs real email",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputCreateUser(invalidEmail)
        # result should contain a user error list with "emailAddress Range" in it
        # and no user should be created
	# TODO: This test does not currently return the right thing
	log.append("For an invalid email: " + str(result))

        wrongTypeEmail = {
	            'emailAddress': 42,
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':None,
	            'dateOfBirth': None,
	            'imagePath':None}
        
        result = inputCreateUser(wrongTypeEmail)
        # result should contain a user error list with "emailAddress Type" in it
        # and no user should be created
        log.append("For wrong type email: " + str(result))

	 #### Password Tests ### #
	noPassword = {
	            'emailAddress':"nyan@gmail.com",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
	
        result = inputCreateUser(noPassword)
	log.append("For no password: " + str(result))

	
	nonePassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':None,
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputCreateUser(nonePassword)
	log.append("For password = None " + str(result))
        
	wrongTypePassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':42,
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputCreateUser(wrongTypePassword)
	log.append("For a password of the wrong type" + str(result))

	tooShortPassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':"donut",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputCreateUser(tooShortPassword)
	log.append("For a password that is too short" + str(result))

	tooLongPassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':"NyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCat", 
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputCreateUser(tooLongPassword)
	log.append("For a password that is too long" + str(result))

	 #### Name Tests ### #
	
	# Name is not in dict
	noName = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(noName)
	log.append("For a dict with no name "+ str(result))

	# Name is wrong type
	wrongTypeName = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':42,
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(wrongTypeName)
	log.append("For a name of the wrong type"+ str(result))

	# Name is too long
	tooLongName = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical SurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(tooLongName)
	log.append("For a name that's too long"+ str(result))

	 #### Image Path Tests ### #

	# Image Path is not in dict
	noPath = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
		}
        result = inputCreateUser(noPath)
	log.append("For a dict with no path"+ str(result))

	# Image Path  is wrong type
	wrongTypeImagePath = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':42}
        result = inputCreateUser(wrongTypeImagePath)
	log.append("For a path of the wrong type: " + str(result))

	#Image path  is too long
	tooLongImagePath = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpghiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiii"}

        result = inputCreateUser(tooLongImagePath)
	log.append("For a path that's too long: " + str(result))

	 #### Date Of Birth Tests ### #

	# dateOfBirth is not in dict
	noDateOfBirth= {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(noDateOfBirth)
	log.append("For a dict with no date of birth: " + str(result))

	# dateOfBirth is wrong type
	wrongTypeDateOfBirth = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':4242,
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(wrongTypeDateOfBirth)
	log.append("For a date of birth of the wrong type: " + str(result))

	# dateOfBirth is too old 
	tooOld = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1899-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(tooOld)
	log.append("For a date of birth that is too old: " + str(result))


	 #### Location Tests ### #

	# Location is not in dict
	noLocation = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(noLocation)
	log.append("For a dict with no location: " + str(result))

	# Location is wrong type
	wrongTypeLocation = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':42,
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(wrongTypeLocation)
	log.append("For a location of the wrong type: " + str(result))

	# Location is too long
	tooLongLocation = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San DiegoSan San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San ",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(tooLongLocation)
	log.append("For a location that's too long: " + str(result))

def TEMP_testLoginBad(log):
	 #### Email Tests ### #

        result = inputLogin(None,"Nyancat")
	log.append("For emailAddress = None: " + str(result))

	result = inputLogin( "Nyan cat needs real email","Nyancat")
	log.append("For an invalid email: " + str(result))

	result = inputLogin( 42,"Nyancat")
        log.append("For wrong type email: " + str(result))

def TEMP_testLogoutBad(log):
	 log.append("There is no input to test for inputLogout()")	

def TEMP_testEditUserBad(log):

	# All the tests from create user
	 #### Email Tests ### #
        emailNone = {
	            'emailAddress':None,
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputEditUser(emailNone)
	log.append("For emailAddress = None: " + str(result))

        noEmail = {
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputEditUser(noEmail)
	log.append("For no email in the dict: " + str(result))

        invalidEmail = {
	            'emailAddress': "Nyan cat needs real email",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputEditUser(invalidEmail)
        # result should contain a user error list with "emailAddress Range" in it
        # and no user should be created
	# TODO: This test does not currently return the right thing
	log.append("For an invalid email: " + str(result))

        wrongTypeEmail = {
	            'emailAddress': 42,
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':None,
	            'dateOfBirth': None,
	            'imagePath':None}
        
        result = inputEditUser(wrongTypeEmail)
        # result should contain a user error list with "emailAddress Type" in it
        # and no user should be created
        log.append("For wrong type email: " + str(result))

	 #### Password Tests ### #
	noPassword = {
	            'emailAddress':"nyan@gmail.com",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
	
        result = inputEditUser(noPassword)
	log.append("For no password: " + str(result))

	
	nonePassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':None,
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputEditUser(nonePassword)
	log.append("For password = None " + str(result))

	wrongTypePassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':42,
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputEditUser(wrongTypePassword)
	log.append("For a password of the wrong type" + str(result))

	tooShortPassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':"donut",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputEditUser(tooShortPassword)
	log.append("For a password that is too short" + str(result))

	tooLongPassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':"NyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCat", 
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputEditUser(tooLongPassword)
	log.append("For a password that is too long" + str(result))

	 #### Name Tests ### #
	
	# Name is not in dict
	noName = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(noName)
	log.append("For a dict with no name "+ str(result))

	# Name is wrong type
	wrongTypeName = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':42,
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(wrongTypeName)
	log.append("For a name of the wrong type"+ str(result))

	# Name is too long
	tooLongName = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical SurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(tooLongName)
	log.append("For a name that's too long"+ str(result))

	 #### Image Path Tests ### #

	# Image Path is not in dict
	noPath = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
		}
        result = inputEditUser(noPath)
	log.append("For a dict with no path"+ str(result))

	# Image Path  is wrong type
	wrongTypeImagePath = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':42}
        result = inputEditUser(wrongTypeImagePath)
	log.append("For a path of the wrong type: " + str(result))

	#Image path  is too long
	tooLongImagePath = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpghiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiii"}

        result = inputEditUser(tooLongImagePath)
	log.append("For a path that's too long: " + str(result))

	 #### Date Of Birth Tests ### #

	# dateOfBirth is not in dict
	noDateOfBirth= {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(noDateOfBirth)
	log.append("For a dict with no date of birth: " + str(result))

	# dateOfBirth is wrong type
	wrongTypeDateOfBirth = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':4242,
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(wrongTypeDateOfBirth)
	log.append("For a date of birth of the wrong type: " + str(result))

	# dateOfBirth is too old 
	tooOld = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1899-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(tooOld)
	log.append("For a date of birth that is too old: " + str(result))


	 #### Location Tests ### #

	# Location is not in dict
	noLocation = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(noLocation)
	log.append("For a dict with no location: " + str(result))

	# Location is wrong type
	wrongTypeLocation = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':42,
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(wrongTypeLocation)
	log.append("For a location of the wrong type: " + str(result))

	# Location is too long
	tooLongLocation = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San DiegoSan San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San ",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(tooLongLocation)
	log.append("For a location that's too long: " + str(result))

	# Malformed dict with bad keys
	 #### Malformed dict ### #
	malformed = {'Cats like':"Donuts"}
	result = inputEditUser(malformed)
	log.append( "With a malformed dict: " + str(result))
	
	# Try to edit my own userID 
	 #### Trying to edit my userID ### #
	userID = {'userID':15}
	result = inputEditUser(userID) 
	log.append( "Editing my own userID: " + str(result))

################ Tests for valid input ########################


def TEMP_testAddUser(log):
	userDict = {
	            'emailAddress':"nyan3@gmail.com",
	            'password':"lolololo",
	            'name':"The Galactical",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
	
	result = inputCreateUser(userDict)
	log.append("Adding a user: " + str(result))
	


def TEMP_testLogin(log):
	# This method assumes the nyan@gmail.com user already exists 
        log.append( "Testing a valid login..."	)
	user = inputLogin("nyan@gmail.com","lololol")
	global thisUser
	thisUser = user[0]
	#print thisUser
	#print "Useras;kdfjasndoh " + str(user)
	#log.append( "Result: " + str(user[0]))
	#log.append("Resultant userID: " + str(user[0].userID) )

def TEMP_testLogout(log):
	# This method assumes the nyan@gmail.com user already exists 
	# and is already logged in
	# Only run this if there is a valid session running
	user = inputLogout()
	log.append( "Result: " + str(user) )
	log.append( "Resultant userID: " + str(user[0].userID) )

def TEMP_testEditUser(log):
	# This method assumes the nyan@gmail.com user already exists 
	# Only run this if there is a valid session running
	changes = {
	            'emailAddress':"changing@gmail.com",
		    'password':"Changed",
	            'name':"Changed Again",
	            'location':"Changeville",
	            'dateOfBirth':"2000-4-1",
	            'imagePath':"changed.jpg"}

	log.append("Result of edit: " + str(inputEditUser(changes)))

	changeBack = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

	log.append("Result of editing user back : " + str(inputEditUser(changeBack)))
	
def TEMP_testAddInventory():
	
	inventoryDict = {'locationName':'Bathtub'}
	                 
	inventoryReturn = inputAddInventory(inventoryDict)
	inventory = inventoryReturn[0]
	#print inventory
	
	
def TEMP_testAddWine():
	wineDict = {'li_wineID':1}
	locationReturn = inputGetLocation(1)
	location = locationReturn[0]
	locationDict = {'locationID':location.locationID}
	
	wineReturn = inputAddWineUser(wineDict, 1, locationDict)
	wine = wineReturn[0]

	#print wine


	

##############################################################################
#    Start Inventory Routing Test Code
##############################################################################

################ Tests on invalid input ###########################
def TEMP_testInputGetWineBad(log):
	log.append("Getting a wine of locationID -1 and wineID -1: " +
		   str(inputGetWine(-1,-1,thisUser)))


	log.append("Getting a wine of locationID 2 and wineID 1000: " +
		   str(inputGetWine(2, 1000,thisUser)))

	log.append("Getting a wine of locationID 1000 and wineID 56" +
		   str(inputGetWine(1000, 56,thisUser)))

	log.append("Getting a wine of locationID 0 and wineID 1, which the user doesn't own" +
		   str(inputGetWine(0, 1,thisUser)))


def TEMP_testInputGetLocationBad(log):
	log.append("Getting a location of bad id -1" +
		   str(inputGetLocation(-1,thisUser)))

	log.append("Getting a location of id not in database 1000" +
		   str(inputGetLocation(1000,thisUser)))

	log.append("Getting a location of id 1, which doesn't belong to user" +
		   str(inputGetLocation(1,thisUser)))
		   
		   
def TEMP_testInputAddWineUserBad(log):
 	#print "First line of testInputAddWineUserBad"
	badWine = {"li_wineID":2,"isWishlist":False, "li_wineID":1, "bitter":-1}
	log.append("Adding wine with malformed value bitter = -1 " +
		   str(inputAddWineUser(badWine, 1, 2,thisUser)))
	#print "PAST THE FIRST"

	badWine = {"li_wineID":2,"isWishlist":False,"description":"testing adding a wine here","qwerty":2}
	log.append("Adding wine with malformed key qwerty = 2 " +
		   str(inputAddWineUser(badWine, 1, 2,thisUser)))

	#print "PAST THE SECOND"

	badWine = {"isWishlist":False,"bitter":0.5}
	log.append("Adding wine with missing li_wineID" +
		   str(inputAddWineUser(badWine, 1, 2,thisUser)))

	#print "PAST THE THIRD"

	badWine = {"isWishlist":False,"li_wineID":1}
	log.append("Adding wine with invalid locationID -1" +
		   str(inputAddWineUser(badWine, 1, -1,thisUser)))

	log.append("Adding wine with invalid count -1" +
		   str(inputAddWineUser(badWine, -1, 2,thisUser)))

	log.append("Adding wine with locationID 1000, which is not in database " +
		   str(inputAddWineUser(badWine, 1, 1000,thisUser)))

	log.append("Adding wine with locationID 1, which doesn't belong to user " +
		   str(inputAddWineUser(badWine, 1, 1,thisUser)))


def TEMP_testInputMoveWineBad(log):
	#print "CALLING INPUT MOVE WINE"
	log.append("Moving wine with invalid ids -1" +
		   str(inputMoveWine(-1, -1, 1,thisUser )))
        #print "Calling the second type of bad moveWine"
	log.append("Moving wine with id not in database 1000" +
		   str(inputMoveWine(1000, 2, 1,thisUser)))
	log.append("Moving wine to location id 1000 not in database" +
		   str(inputMoveWine(56, 1000, 1,thisUser)))

	# CHECK
	log.append("Moving wine with id 1 which doesn't belong to user: " +
		   str(inputMoveWine(1, 2, 1,thisUser)))

	log.append("Moving wine with invalid count -1: " +
		   str(inputMoveWine(56, 2, -1,thisUser)))


def TEMP_testInputAddInventoryBad(log):
	location = {"lm_userID":-1}
	log.append("Adding inventory with malformed user id -1" +
		   str(inputAddInventory(thisUser, location)))
		   
	log.append("Adding inventory with empty location dict" +
		   str(inputAddInventory(thisUser, {})))
		   
		   
def TEMP_testInputDeleteWineUserBad(log):
	try:
		if DEBUG:
			print "Trying with invalid ID"
		log.append("Deleting wine with invalid id -1" +
		   str(inputDeleteWineUser(thisUser, -1,2)))
		   
	except:
		view_traceback()	
		exit(0)
		   
		  
def TEMP_testInputDeleteInventoryBad(log):
	log.append("Deleting inventory with invalid id -1" +
		   str(inputDeleteInventory(-1,thisUser)))
		   
	log.append("Deleting inventory with unassigned id 1000" +
		   str(inputDeleteInventory(1000,thisUser)))
		   
		   
def TEMP_testInputEditInventoryBad(log):
	changes = {"imagePath":None}
	log.append("Editing inventory with invalid id -1" +
		   str(inputEditInventory(-1, changes)))
		   
	log.append("Editing inventory with id 1000 not in database" +
		   str(inputEditInventory(1000, changes)))
		   
	changes = {"imagePath":-1}
	log.append("Editing inventory with malformed value imagePath = -1" +
		   str(inputEditInventory(2, changes)))
		   
	changes = {"squiggly":5}
	log.append("Editing inventory with malformed key squiggly = 5" +
		   str(inputEditInventory(2, changes)))
		   
	changes = {}
	log.append("Editing inventory with empty changes" +
		   str(inputEditInventory(2, changes)))
		   
		   
def TEMP_testInputEditEntryUserBad(log):
	changes = {"bitter":.2}
	log.append("Editing wine entry with invalid id -1" +
		   str(inputEditEntryUser(-1, -1, changes)))
		   
	log.append("Editing wine entry with id not in database 1000" +
		   str(inputEditEntryUser(2, 1000, changes)))
		   
	changes = {"bitter":-2}
	log.append("Editing wine entry with malformed value bitter = -1" +
		   str(inputEditEntryUser(2, 56, changes)))
		   
	changes = {"squiggly":1}
	log.append("Editing wine entry with malformed key squiggly = 1" +
		   str(inputEditEntryUser(2, 56, changes)))
		   
	changes = {}
	log.append("Editing wine entry with empty changes" +
		   str(inputEditEntryUser(2, 56, changes)))
		   
		   
def TEMP_testInputViewArchiveBad(log):
	log.append("Viewing archive with invalid id -1" +
		   str(inputViewArchive(-1,thisUser)))
		   
	log.append("Viewing archive with unassigned id 1000" +
		   str(inputViewArchive(1000,thisUser)))


def TEMP_testInputRateWineUserBad(log):
	log.append("Rating wine with invalid id -1" +
		   str(inputRateWineUser(2, -1, 3,thisUser)))
		   
	log.append("Rating wine with unassigned id 1000" +
		   str(inputRateWineUser(2, 1000, 3,thisUser)))
		   
	log.append("Rating wine with invalid rating -1" +
		   str(inputRateWineUser(2, 56, -1,thisUser)))


################ Tests on valid input ###########################
def TEMP_testInputGetWine(log):
	#print "\ttestInputGetWIne"
        log.append("Getting a wine of locationID 2 and wineID 465: " +
	           str(inputGetWine(2,465,thisUser)))
def TEMP_testInputGetWineGlobal(log):
	log.append("Getting a global wine of id 1: " +
		str(inputGetWineGlobal(1)))
        

def TEMP_testInputGetLocation(log):
	#print "\ttestINputGetLocation"
        log.append("Getting a location of locationID 2: " +
                   str(inputGetLocation(2,thisUser)))

def TEMP_testInputGetUserLocations(log):
	#print "\ttestInputGetUserLocations"
        log.append("Getting that user's locations: " +
                    str(inputGetUserLocations(thisUser)))

def TEMP_testInputGetLocationHistory(log):
	#print "\ttestInputGetLocationHistory"
        log.append("Getting a location history: " +
                   str(inputGetLocationHistory(2,56,thisUser)))

def TEMP_testInputGetInventory(log, thisUser):
	#print "\ttestinputGetInventory"
        log.append("Gettin an inventory: " +
                   str(inputGetInventory(thisUser)))


def TEMP_testInputAddWineUser(log):
	#print "\ttestInputAddWineUser"
        validLocationID = 2
        validWine = {
	  'li_wineID': 1,
	  'li_locationID':validLocationID,
          'quantity':2,
 	  'description':"Look! I can add a wine!",
          'personalStarRating':5,
          'isWishlist':False,
          'bitter':1.1,
          'sweet':1.1,
          'sour':1.1,
          'salty':1.1,
          'chemical':1.1,
          'pungent':1.1,
          'oxidized':1.1,
          'microbiological':1.1,
          'floral':1.1,
          'spicy':1.1,
          'fruity':1.1,
          'vegetative':1.1,
          'nutty':1.1,
          'caramelized':1.1,
          'woody':1.1,
          'earthy':1.1}


        count = 2

        log.append("Adding a valid wine: " +
                    str(inputAddWineUser(validWine,count,validLocationID,thisUser)))
          

def TEMP_testInputMoveWine(log):
	#print "\ttestInputMoveWine"
        log.append("Moving a wine: " +
                   str(inputMoveWine(465,10,1,thisUser,False)))

def TEMP_testInputAddInventory(log):
	#print "\ttestInputAddInventory"
        # make a location dictionary
        location = {
          'lm_userID':int(request.cookies.get('username')),
          'locationName':"New Inventory. Woo!",
          'timeCreated': str(datetime.now().replace(microsecond = 0)),
          'imagePath':"Fake.jpg"
        }
        log.append("Adding a location: " + str(inputAddInventory(thisUser,location)))
          

def TEMP_testInputDeleteWineUser(log):
	if DEBUG:
		print "\ttestInputDeleteWineUser"
        log.append("Deleting 1 wine of id 56: " +
                   str(inputDeleteWineUser(thisUser,56,2)))

def TEMP_testInputDeleteInventory(log):
	#print "\ttestInputDeleteInventory"
        log.append("Deleting an inventory of id 11: " +
                   str(inputDeleteInventory(11,thisUser)))

def TEMP_testInputEditInventory(log):
	#print "\ttestInputEditInventory"
        changes = {
          'locationName':"Kitchen",
          'imagePath':"Fake.jpg"}

        log.append("Editing an inventory of locationID 2: " +
                   str(inputEditInventory(2,changes,thisUser)))

def TEMP_testInputEditEntryUser(log):
	#print "\ttestInputEditEntryUser"
        changes = {
          'li_locationID': 2,
          'quantity':2,
          'personalStarRating':5,
          'isWishlist':False,
          'bitter':1.1,
          'sweet':1.1,
          'sour':1.1,
          'salty':1.1,
          'chemical':1.1,
          'pungent':1.1,
          'oxidized':1.1,
          'microbiological':1.1,
          'floral':1.1,
          'spicy':1.1,
          'fruity':1.1,
          'vegetative':1.1,
          'nutty':1.1,
          'caramelized':1.1,
          'woody':1.1,
          'earthy':1.2}

        log.append("Editing a wine of id 56: " +
                   str(inputEditEntryUser(2,56,changes,thisUser)))

def TEMP_testImportInventory(log):
        log.append("Not testing xml import at this time")

def TEMP_testExportInventory(log):
        log.append("Not testing xml inventory export at this time")

def TEMP_testInputViewStats(log):
	#print "\ttestInputViewStats"
        log.append("Not testing view stats at this time")

def TEMP_testInputViewArchive(log):
	#print "\t testInputViewArchive"
        log.append("Viewing the archive for location of id 2: " +
                   str(inputViewArchive(2,thisUser)))

def TEMP_testInputRateWineUser(log):
	#print "\ttestInputRateWineUser"
        log.append("Rating a wine of ID 56: " +
                   str(inputRateWineUser(2,56,1,thisUser)))



#The User Object
def TEMP_makeTestUser():
	user = UserInfo(1234,
					"nyan@gmail.com",
					"Nyancat",
					"The Galactical Surfline",
					None,
					None,
					None)
	#print user
	return user


#A List of Wines from a User's Inventory
def TEMP_makeFakeInventory(user):

	#print 'Loading Test Inventory...'
	tags = makeSimpleTagList()
	inventory = []
	
	for i in range(0, 10):
		wine = LocationInventory(i,
		                         i,
		                         i,
		                         random.randrange(0,5),
		                         tags[(i+3) % 7 % len(tags)] + ',' + tags[i % 11 % len(tags)],
		                         'THIS IS NONSENSE......lawl',
		                         'wine' + str(i%14) + '.jpeg',
		                         random.randrange(0, 5),
		                         0,
		                         random.uniform(0.0, 1.5),
              				 	 random.uniform(0.0, 1.5),
               				 	 random.uniform(0.0, 1.5),
						         random.uniform(0.0, 1.5),
                                 random.uniform(0.0, 1.5),
                                 random.uniform(0.0, 1.5),
                                 random.uniform(0.0, 1.5),
                                 random.uniform(0.0, 1.5),
                                 random.uniform(0.0, 1.5),
                                 random.uniform(0.0, 1.5),
                                 random.uniform(0.0, 1.5),
                                 random.uniform(0.0, 1.5),
                                 random.uniform(0.0, 1.5),
                                 random.uniform(0.0, 1.5),
                                 random.uniform(0.0, 1.5),
                                 random.uniform(0.0, 1.5))
		inventory.append(wine)
		#print wine

	#print inventory
	#print 'End Loading Test Inventory.'
	return inventory

#A List of Wines (Wine Objects)
def TEMP_makeFakeWineList():

	# #print 'Making Fake Wine List'
	tags = makeSimpleTagList()
	wines = []

	for i in range(0, 20):
		wine = Wine(i,
	               "Wine  #" + str(i),
	               "Varietal  #" + str(i),
	               "Winery  #" + str(i),
	               "Wine Type  #" + str(i),
	               (1990 + i),
	               "Region " + str(unichr(i)),
	               None,
	               None,
	               tags[(i+3) % 7 % len(tags)] + ',' + tags[i % 11 % len(tags)],
	               "Best Wine Evar, or at least so we hope! BTW, Mershed Perderders are like teh bestest n'stuff!111!1!",
	               random.randrange(1,6),
	               None,
	               None,
	               random.uniform(0.0, 1.5),
	               random.uniform(0.0, 1.5),
	               random.uniform(0.0, 1.5),
	               random.uniform(0.0, 1.5),
	               random.uniform(0.0, 1.5),
	               random.uniform(0.0, 1.5),
	               random.uniform(0.0, 1.5),
	               random.uniform(0.0, 1.5),
	               random.uniform(0.0, 1.5),
	               random.uniform(0.0, 1.5),
	               random.uniform(0.0, 1.5),
	               random.uniform(0.0, 1.5),
	               random.uniform(0.0, 1.5),
	               random.uniform(0.0, 1.5),
	               random.uniform(0.0, 1.5),
	               random.uniform(0.0, 1.5))
		wines.append(wine)
		##print wine.tags
		##print wine

	##print wines
	##print 'End making fake wine list.'
	return wines

#Constructs a simple List of Tags (Strings) for use 
#in building test wines
def makeSimpleTagList():
	tags = list()
	tags.append("Cinnamon")
	tags.append("Orange")
	tags.append("Pineapple")
	tags.append("Coconut")
	tags.append("Bacon")
	tags.append("Steak")
	tags.append("Honey")
	tags.append("Cedar")
	tags.append("Honeyed Cucumber")
	tags.append("Cat Food")
	tags.append("Carrot")
	tags.append("Forest Moss")
	tags.append("Avacado")
	tags.append("Tuxedo")
	tags.append("Vanilla")
	tags.append("Nutmeg")

	#print tags
	return tags

#A List of Locations (Strings) UNIQUE
def TEMP_makeLocationsListFromInventory(inventory):
	items = list()
	for wine in inventory:
		items.append(wine.li_locationID)
	#print items
	return OrderedDict.fromkeys(items).keys()

#A List of Filters (Strings) UNIQUE
def TEMP_makeTypeFiltersFromWines(wines):
	items = list()
	for wine in wines:
		items.append(wine.wineType)
	#print items
	return OrderedDict.fromkeys(items).keys()

#A List of Varietals (String) UNIQUE
def TEMP_makeVarietalFiltersFromWines(wines):
	items = list()
	for wine in wines:
		items.append(wine.varietal_blend)
	#print items
	return OrderedDict.fromkeys(items).keys()

#A List of Wineries (Strings) UNIQUE
def TEMP_makeWineryFiltersFromWines(wines):
	items = list()
	for wine in wines:
		items.append(wine.winery)
	#print items
	return OrderedDict.fromkeys(items).keys()

#A List of Tags (Strings) UNIQUE
def makeTagListFromWines(inventory):
	items = []
	for wine in inventory:
		tagString = wine.tags
		#print tagString
		tagsNaked = tagString.strip()
		#print tagsNaked
		tagList = tagsNaked.split(',')
		#print tagList
		for tag in tagList:
			items.append(tag)
	#print items
	return OrderedDict.fromkeys(items).keys()



if __name__ == '__main__':
	app.run(host='0.0.0.0', port='9235')
