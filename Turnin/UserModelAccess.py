from flask import *
from Classes import *
from InstantiationValidation import *
import Globals
from sqlalchemy import *
import random
import sys
import datetime
import DBAccessConnection



def dbGetUser(userID):
  """Retrieve a user's profile from database
  Retrieve relevant information about a user from the database.
  Return a dictionary representing the user.

  Args:
   int userID: The userID of the user being retrieved.
  
  Return:
   UserInfo: A UserInfo object specifying relevant information about the user. Store enough
             information to generate a user profile page.
  """
  err = []
  sysErr = []
  try:
    user = DBAccessConnection.userInfo.select(DBAccessConnection.userInfo.c.userID == userID).execute().first()
    user2 = UserInfo(user.userID, user.emailAddress, user.password, user.name, user.location, user.dateOfBirth, user.imagePath)
  except:
    err.append("dbGetUser Error found")
  if not err and not sysErr:
    return (user2, None)
  else:
    return (None, (err, sysErr))

def dbDoesUserExist(email):
  """Method to check if user exists in database

  Args: 
    string email: The email entered

  Return:
    bool: True if user exists in database, False otherwise
  """
  err = []
  sysErr = []
  try:
    user = DBAccessConnection.userInfo.select(DBAccessConnection.userInfo.c.emailAddress == email).execute().first()
  except:
    sysErr.append("dbDoesUserExist Error found")
  if user is not None and err is not None and sysErr is not None:
    return True
  else:
    return False

def dbLogin(email, password):
  """Method to authorize a user login. The user's email and password are queried, and if there is a match, the login proceeds

  Args:
    string email: The entered email
    string password: The entered password

  Return:
    UserInfo: The UserInfo object associated with the entered email and password
  """
  err = []
  sysErr = []
  user = DBAccessConnection.userInfo.select(DBAccessConnection.userInfo.c.emailAddress == email).execute().first()
  if user is None:
    err.append("Invalid E-mail Address")
    return (None, (err,sysErr))
  elif (user['password'] == password):
    user1 = UserInfo(user.userID, user.emailAddress, user.password, user.name, user.location, user.dateOfBirth, user.imagePath)
    return (user1, None)
  else:
    err.append("Incorrect password")
    return (None, (err,sysErr))

def dbCreateUser(user):
  """Add new user to database
  Insert a new user into the database.

  Args:
    UserInfo user: UserInfo object representing the user. Take all fields from this object.
  
  Return:
    UserInfo: The user just added to the database.
 """
  err = []
  sysErr = []
  try:
    user1 = DBAccessConnection.userInfo.select(DBAccessConnection.userInfo.c.emailAddress == user.emailAddress).execute().first()
  except:
    sysErr.append('User Already Exists check has Failed')
    
  if user1 is None:
    try:
      DBAccessConnection.con.execute(DBAccessConnection.userInfo.insert(), emailAddress = user.emailAddress, password = user.password, name = user.name, location = user.location, dateOfBirth = user.dateOfBirth, imagePath = user.imagePath)
      user2 = DBAccessConnection.userInfo.select(DBAccessConnection.userInfo.c.emailAddress == user.emailAddress).execute().first()
      user3 = UserInfo(user2['userID'],user2['emailAddress'],user2['password'],user2['name'],user2['location'],user2['dateOfBirth'],user2['imagePath'])
    except:
      sysErr.append("dbCreateUser Error found")
  else:
    sysErr.append("E-mail address already in database")
    return (None, (err,sysErr))
  if (len(err) == 0 and len(sysErr) == 0):
   	return (user3,(err,sysErr))
  else:
   	return (None, (err,sysErr))


def dbEditUser(user):
  """Update user profile in database with attributes
  Change information stored about the user in the database to match the user object argument.

  Args:
    UserInfo user: UserInfo object representing the user. Changes have already been applied.

  Return:
    UserInfo: The user just modified
  """
  err = []
  sysErr = []
 
  try:
    DBAccessConnection.con.execute(DBAccessConnection.userInfo.update(DBAccessConnection.userInfo.c.userID==user.userID), emailAddress=user.emailAddress, 
              password = user.password, name = user.name, location = user.location, 
              dateOfBirth = user.dateOfBirth, imagePath = user.imagePath)
  except:
    err.append('Account Edit Failed')
  
  return (user, (err, sysErr))


def dbDeleteUser(user):
  """Delete the user profile for the user represented by the user object argument.

  Args:
    UserInfo user: UserInfo object representing the user to delete from the database.

  Return:
    UserInfo: The user just deleted from the database.
  """
  
  """ DESIGN DECISION: Currently this method must delete all data associated with the user
      because the userID field is a primary key in UserInfo and a foreign key elsewhere. If
      we want to retain user data we would add a "deleted" flag column to the UserInfo table
      and set that bit upon a delete request. A user with the delete flag set would not be
      allowed to login and would not be visible in any way to any user, but their data could
      still be used by system algorithms.
  """
  
  
  err = []
  sysErr = []
  
  try:
    DBAccessConnection.con.execute("DELETE FROM RecommenderHistory "
              + "WHERE rh_recommenderID IN ( "
              +   "SELECT r.recommenderID "
              +   "FROM Recommenders r "
              +   "WHERE r.r_userID = " + str(user.userID) + " )")
    DBAccessConnection.con.execute("DELETE FROM LocationHistory "
              + "WHERE lh_locationID IN ( "
              +   "SELECT lm.locationID "
              +   "FROM LocationMap lm "
              +   "WHERE lm.lm_userID = " + str(user.userID) + " )")
    DBAccessConnection.con.execute("DELETE FROM LocationInventory "
              + "WHERE li_locationID IN ( "
              +   "SELECT lm.locationID "
              +   "FROM LocationMap lm "
              +   "WHERE lm.lm_userID = " + str(user.userID) + " )")
    DBAccessConnection.con.execute(DBAccessConnection.locationMap.delete(DBAccessConnection.locationMap.c.lm_userID==user.userID))
    DBAccessConnection.con.execute(DBAccessConnection.recommenders.delete(DBAccessConnection.recommenders.c.r_userID==user.userID))
    DBAccessConnection.con.execute(DBAccessConnection.userInfo.delete(DBAccessConnection.userInfo.c.userID==user.userID))
  except:
    err.append('User Deletion Failed')
  
  return (user, (err, sysErr))
