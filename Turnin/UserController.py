"""User account module
"""

from Classes import *
from InstantiationValidation import *
from UserModelAccess import *
from InventoryModelAccess import *
from RecommenderModelAccess import *
import Globals


def createUser(user):
  """Add the user to database
  
  Args:
    dict user: Dict representing the UserInfo object of the potential new user
    
  Return:
    UserInfo: The newly created user object
  """
  return dbCreateUser(user)

def login(email, password):
  """Login the user
     Called after being validated by Login.py
  
  Args:
    string username: The potential username
    string password: The potential password
    
  Return:
    UserInfo: UserInfo object of the logged in user
  """
  return dbLogin(email, password)

def logout():
  """Logout user
  
  Args:
    UserInfo user: UserInfo object of the user being logged out.
    
  Return:
    UserInfo: The UserInfo object representing the user.
  """

  #What is this used for exactly?

  #userID = request.cookies.get('username')
  return dbGetUser(userID)

def doesUserExist(email):
  exists = dbDoesUserExist(email)
  return exists
  

def editUser(user, attr):
  """Call DataAccess layer to update user profile in database with attributes
  
  Change information stored about the user in the database to match relevant information
  passed in attr.
  
  Args:
    dict attr: A dict specifying user attributes, of the form {email:*, DOB:*, etc}. Not every
               field stored in the database has to be present.
               
  Return:
    UserInfo: The updated UserInfo object representing the user.
  """
  #userID = request.cookies.get('username') 
  #user = dbGetUser(userID)[0]
 
  try: 
    for key, value in attr.items():
      user.__dict__[key] = value
  
    return dbEditUser(user)
  except:
    return (None, (None, ["Exception encountered"]))


def deleteUser(user):
  """ Deletes a User from the Database
  
  Args:
    UserInfo user: UserInfo object representing the user to delete.
    
  Return:
    UserInfo: UserInfo object representing the removed user.
  """
  return dbDeleteUser(user)
