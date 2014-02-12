from Classes import *
from InstantiationValidation import *
from InventoryIOController import *
from UserIOController import *
from flask import *
from collections import OrderedDict
import random



##############################################################################
#    Start General Inv Test Code
##############################################################################


################ Tests for invalid input ######################

def TEMP_testAddUserBad():

	print "\n#### Email Tests ####"
        emailNone = {
	            'emailAddress':None,
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputCreateUser(emailNone)
	print "For emailAddress = None: " + str(result)

        noEmail = {
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputCreateUser(noEmail)
	print "For no email in the dict: " + str(result)

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
	print "For an invalid email: " + str(result)

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
        print "For wrong type email: " + str(result)

	print "\n#### Password Tests ####"
	noPassword = {
	            'emailAddress':"nyan@gmail.com",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
	
        result = inputCreateUser(noPassword)
	print "For no password: " + str(result)

	
	nonePassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':None,
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputCreateUser(nonePassword)
	print "For password = None " + str(result)
        
	wrongTypePassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':42,
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputCreateUser(wrongTypePassword)
	print "For a password of the wrong type" + str(result)

	tooShortPassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':"donut",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputCreateUser(tooShortPassword)
	print "For a password that is too short" + str(result)

	tooLongPassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':"NyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCat", 
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputCreateUser(tooLongPassword)
	print "For a password that is too long" + str(result)

	print "\n#### Name Tests ####"
	
	# Name is not in dict
	noName = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(noName)
	print "For a dict with no name "+ str(result)

	# Name is wrong type
	wrongTypeName = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':42,
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(wrongTypeName)
	print "For a name of the wrong type"+ str(result)

	# Name is too long
	tooLongName = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical SurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(tooLongName)
	print "For a name that's too long"+ str(result)

	print "\n#### Image Path Tests ####"

	# Image Path is not in dict
	noPath = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
		}
        result = inputCreateUser(noPath)
	print "For a dict with no path"+ str(result)

	# Image Path  is wrong type
	wrongTypeImagePath = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':42}
        result = inputCreateUser(wrongTypeImagePath)
	print "For a path of the wrong type: " + str(result)

	#Image path  is too long
	tooLongImagePath = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpghiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiii"}

        result = inputCreateUser(tooLongImagePath)
	print "For a path that's too long: " + str(result)

	print "\n#### Date Of Birth Tests ####"

	# dateOfBirth is not in dict
	noDateOfBirth= {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(noDateOfBirth)
	print "For a dict with no date of birth: " + str(result)

	# dateOfBirth is wrong type
	wrongTypeDateOfBirth = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':4242,
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(wrongTypeDateOfBirth)
	print "For a date of birth of the wrong type: " + str(result)

	# dateOfBirth is too old 
	tooOld = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1899-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(tooOld)
	print "For a date of birth that is too old: " + str(result)


	print "\n#### Location Tests ####"

	# Location is not in dict
	noLocation = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(noLocation)
	print "For a dict with no location: " + str(result)

	# Location is wrong type
	wrongTypeLocation = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':42,
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(wrongTypeLocation)
	print "For a location of the wrong type: " + str(result)

	# Location is too long
	tooLongLocation = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San DiegoSan San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San ",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputCreateUser(tooLongLocation)
	print "For a location that's too long: " + str(result)

def TEMP_testLoginBad():
	print "\n#### Email Tests ####"

        result = inputLogin(None,"Nyancat")
	print "For emailAddress = None: " + str(result)

	result = inputLogin( "Nyan cat needs real email","Nyancat")
	print "For an invalid email: " + str(result)

	result = inputLogin( 42,"Nyancat")
        print "For wrong type email: " + str(result)

def TEMP_testLogoutBad():
	print "\nThere is no input to test for inputLogout()"	

def TEMP_testEditUserBad():
	# All the tests from create user
	print "\n#### Email Tests ####"
        emailNone = {
	            'emailAddress':None,
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputEditUser(emailNone)
	print "For emailAddress = None: " + str(result)

        noEmail = {
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputEditUser(noEmail)
	print "For no email in the dict: " + str(result)

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
	print "For an invalid email: " + str(result)

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
        print "For wrong type email: " + str(result)

	print "\n#### Password Tests ####"
	noPassword = {
	            'emailAddress':"nyan@gmail.com",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
	
        result = inputEditUser(noPassword)
	print "For no password: " + str(result)

	
	nonePassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':None,
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputEditUser(nonePassword)
	print "For password = None " + str(result)
        
	wrongTypePassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':42,
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputEditUser(wrongTypePassword)
	print "For a password of the wrong type" + str(result)

	tooShortPassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':"donut",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputEditUser(tooShortPassword)
	print "For a password that is too short" + str(result)

	tooLongPassword= {
	            'emailAddress':"nyan@gmail.com",
	            'password':"NyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCatNyanCat", 
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

        result = inputEditUser(tooLongPassword)
	print "For a password that is too long" + str(result)

	print "\n#### Name Tests ####"
	
	# Name is not in dict
	noName = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(noName)
	print "For a dict with no name "+ str(result)

	# Name is wrong type
	wrongTypeName = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':42,
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(wrongTypeName)
	print "For a name of the wrong type"+ str(result)

	# Name is too long
	tooLongName = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical SurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurflineSurfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(tooLongName)
	print "For a name that's too long"+ str(result)

	print "\n#### Image Path Tests ####"

	# Image Path is not in dict
	noPath = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
		}
        result = inputEditUser(noPath)
	print "For a dict with no path"+ str(result)

	# Image Path  is wrong type
	wrongTypeImagePath = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':42}
        result = inputEditUser(wrongTypeImagePath)
	print "For a path of the wrong type: " + str(result)

	#Image path  is too long
	tooLongImagePath = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpghiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiiihiiiii"}

        result = inputEditUser(tooLongImagePath)
	print "For a path that's too long: " + str(result)

	print "\n#### Date Of Birth Tests ####"

	# dateOfBirth is not in dict
	noDateOfBirth= {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(noDateOfBirth)
	print "For a dict with no date of birth: " + str(result)

	# dateOfBirth is wrong type
	wrongTypeDateOfBirth = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':4242,
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(wrongTypeDateOfBirth)
	print "For a date of birth of the wrong type: " + str(result)

	# dateOfBirth is too old 
	tooOld = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1899-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(tooOld)
	print "For a date of birth that is too old: " + str(result)


	print "\n#### Location Tests ####"

	# Location is not in dict
	noLocation = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(noLocation)
	print "For a dict with no location: " + str(result)

	# Location is wrong type
	wrongTypeLocation = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':42,
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(wrongTypeLocation)
	print "For a location of the wrong type: " + str(result)

	# Location is too long
	tooLongLocation = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San DiegoSan San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San San ",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
        result = inputEditUser(tooLongLocation)
	print "For a location that's too long: " + str(result)

	# Malformed dict with bad keys
	print "\n#### Malformed dict ####"
	malformed = {'Cats like':"Donuts"}
	result = inputEditUser(malformed)
	print "With a malformed dict: " + str(result)
	
	# Try to edit my own userID 
	print "\n#### Trying to edit my userID ####"
	userID = {'userID':15}
	result = inputEditUser(userID) 
	print "Editing my own userID: " + str(result)



################ Tests for valid input ########################


def TEMP_testAddUser():
	userDict = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}
	
	result = inputCreateUser(userDict)
	print "HIIIIII"
	print result
	
	loginReturn = inputLogin('nyan@gmail.com', 'Nyancat')
	print "YOOOOOOO"
	if loginReturn[0] == None:
		print loginReturn[1]
		return

	user = loginReturn[0]
	session['username'] = user.userID
	print session['username']

def TEMP_testLogin():
	# This method assumes the nyan@gmail.com user already exists 
        print "Testing a valid login..."	
	user = inputLogin("nyan@gmail.com","Nyancat")
	print "Result: " + str(user[0])
	print "Resultant userID: " + str(user[0].userID) 
	print "Resultant email: " + user[0].emailAddress 
	print "Resultant password: " + user[0].password
	print "Resultant name: " + user[0].name
	print "Resultant location: " + user[0].location 
	print "Resultant DOB: " + str(user[0].dateOfBirth) 
	print "Resultant imagePath: " + user[0].imagePath 

def TEMP_testLogout():
	# This method assumes the nyan@gmail.com user already exists 
	# and is already logged in
	# Only run this if there is a valid session running
        print "Testing a valid logout..."	
	user = inputLogout()
	print "Result: " + str(user) 
	print "Resultant userID: " + str(user[0].userID) 
	print "Resultant email: " + user[0].emailAddress 
	print "Resultant password: " + user[0].password
	print "Resultant name: " + user[0].name
	print "Resultant location: " + user[0].location 
	print "Resultant DOB: " + str(user[0].dateOfBirth) 
	print "Resultant imagePath: " + user[0].imagePath 

def TEMP_testEditUser():
	# This method assumes the nyan@gmail.com user already exists 
	# Only run this if there is a valid session running
	changes = {
	            'emailAddress':"changing@gmail.com",
		    'password':"Changed",
	            'name':"Changed Again",
	            'location':"Changeville",
	            'dateOfBirth':"2000-4-1",
	            'imagePath':"changed.jpg"}

	print "Testing editing a user..."
	print "Result: " + str(inputEditUser(changes))

	changeBack = {
	            'emailAddress':"nyan@gmail.com",
	            'password':"Nyancat",
	            'name':"The Galactical Surfline",
	            'location':"San Diego",
	            'dateOfBirth':"1999-4-1",
	            'imagePath':"hiiiii.jpg"}

	print "Putting the user back to it's original state..."
	print "Result: " + str(inputEditUser(changeBack))
	
	
def TEMP_testAddInventory():
	
	inventoryDict = {'locationName':'Bathtub'}
	                 
	inventoryReturn = inputAddInventory(inventoryDict)
	inventory = inventoryReturn[0]
	print inventory
	
	
def TEMP_testAddWine():
	wineDict = {'li_wineID':1}
	locationReturn = inputGetLocation(1)
	location = locationReturn[0]
	locationDict = {'locationID':location.locationID}
	
	wineReturn = inputAddWineUser(wineDict, 1, locationDict)
	wine = wineReturn[0]

	print wine

def TEMP_testInputGetWine():
        result = inputGetWine(1,1)
        # should return the wine created in testAddWine
        print result

def TEMP_testInputGetLocationHistory():
        result = inputGetLocationHistory(1,1)
        # should return a location history object for the wines added
        print result
	

##############################################################################
#    Start Inventory Routing Test Code
##############################################################################

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
def TEMP_makeFakeWineList(inventory):

	#print 'Making Fake Wine List'
	tags = makeSimpleTagList()
	wines = []

	for i in range(0, 20):
		wine = Wine(i,
	               "Wine #" + str(i),
	               "Varietal #" + str(i),
	               "Winery #" + str(i),
	               "Wine Type #" + str(i),
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
		#print wine.tags
		#print wine

	#print wines
	#print 'End making fake wine list.'
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
		items.append(wine['user_li_locationID'])
	#print items
	return OrderedDict.fromkeys(items).keys()

#A List of Filters (Strings) UNIQUE
def TEMP_makeTypeFiltersFromWines(wines):
	items = list()
	for wine in wines:
		items.append(wine['wine_wineType'])
	#print items
	return OrderedDict.fromkeys(items).keys()

#A List of Varietals (String) UNIQUE
def TEMP_makeVarietalFiltersFromWines(wines):
	items = list()
	for wine in wines:
		items.append(wine['wine_varietal'])
	#print items
	return OrderedDict.fromkeys(items).keys()

#A List of Wineries (Strings) UNIQUE
def TEMP_makeWineryFiltersFromWines(wines):
	items = list()
	for wine in wines:
		items.append(wine['wine_winery'])
	#print items
	return OrderedDict.fromkeys(items).keys()

#A List of Wineries (Strings) UNIQUE
def TEMP_makeVintageFiltersFromWines(wines):
	items = list()
	for wine in wines:
		items.append(wine['wine_vintage'])
	#print items
	return OrderedDict.fromkeys(items).keys()

#A List of Tags (Strings) UNIQUE
def makeTagListFromWines(inventory):
	items = list()
	for wine in inventory:
		tagString = wine['user_tags']
		if tagString == None or tagString.strip() == '':
			continue
		#print tagString
		tagsNaked = tagString.strip()
		#print tagsNaked
		tagList = tagsNaked.split(',')
		#print tagList
		for tag in tagList:
			if tag.strip() != '':
				items.append(tag.strip())
	#print items
	return OrderedDict.fromkeys(items).keys()
