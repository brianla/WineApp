"""User login preprocessing module
"""

from Classes import *
import Globals
from User import *
import datetime
import re

def inputCreateUser(dictUser):
  """Preprocess new user info
  
  Args:
    dict dictUser: Dict representing all fields of a UserInfo object
    
  Return:
    A tuple of :
      UserInfo: The newly created user object
      tuple: a tuple of a user error list and a system error list
  """
  # Make an empty error list
  err = []

  print 'inputCreateUser: about to verify'
  result = verifyUser(dictUser)
  print 'inputCreateUser: mad it through verify'

  if result[0] == None:
    print 'Unable to create user'
    return result
  ##else
  #  result = result[0]

  # All checks completed. Make and return UserInfo object
  #if not err:
  return createUser(result[0])



def inputLogin(email, password):
  """Preprocess login information
  
  Args:
    string username: The potential username
    string password: The potential password
    
  Return:
    A tuple of:
      UserInfo: UserInfo object of the logged in user
      dict: an error list
  """
  # Make an empty error list
  err = []
  
  # check the username
  if email == None:
    err.append('email' + ' ' + 'None')
    return (None, (err, None))
  # type check
  if not isinstance(email, basestring):
    err.append('email' + ' ' + 'Type')
    return (None, (err, None))
  if re.match(r"[^@]+@[^@]+\.[^@]+", email) == None:
    err.append('email' + ' ' + "Range")
    return (None, (err, None))
  # email must be < 255
  if len(email) > 255:
      err.append('email' + ' ' + 'Range')
      return (None, (err, None))

  # check the password
  if password == None:
    err.append('password' + ' ' + 'None')
    return (None, (err, None))

  #type check
  if not isinstance(password, basestring):
    err.append('password' + ' ' + 'Type')
    return (None, (err, None))
  # passwords must be > 6 characters but not > 255
  if len(password) < 6 or len(password) > 255:
    err.append('password' + ' ' + 'Range')
    return (None, (err, None))



  if not err:
    return login(email, password)


  

def inputLogout():
  """Preprocess logout
  
  Args:
  """
  return logout()
  
  
def inputEditUser(user, attr):
  """Preprocess updating user profile
  
  Args:
  dict attr: A dict specifying user attributes, of the form {email:*, DOB:*, etc}. Not every
               field stored in the database has to be present.
  """
  
  # Make an empty error list
  
  attr['emailAddress'] = user.emailAddress
  result = verifyUser(attr)
  del attr['emailAddress']

  if result[0] == None:
    return result
  ##else
    ##result = result[0]

  ##if not result[1] or not result[1][0]:
  return editUser(user, attr)



def inputDeleteUser(user):
  """ Deletes a User from the Database """
  return deleteUser(user)


def verifyUser(dictUser):

    # NOTE: if any variable is None a type error will appear in the err list
  
  # initalize all attributes to None to give them scope needed
  # to make a user outside of the try-except blocks
  err = []

  userID = None
  emailAddress = None
  password = None
  name = None
  location = None
  dateOfBirth = None
  imagePath = None
  
  # check the email address
  try:
    emailAddress = dictUser['emailAddress']
    print type(emailAddress)
    if not isinstance(emailAddress, basestring):
      err.append('emailAddress' + ' ' + "Type")
      return (None, (err, None))
    # regex match to check for valid email
    if re.match(r"[^@]+@[^@]+\.[^@]+", emailAddress) == None:
      err.append('emailAddress' + ' ' + "Range")
      return (None, (err, None))
  except KeyError:
    emailAddress = None
    err.append('emailAddress' + ' ' + 'None')
    # a user must have an email address
    return (None, (err, None))
    
  # check the password
  try:
    password = dictUser['password']
    #type check
    if not isinstance(password, basestring):
      err.append('password' + ' ' + 'Type')
      return (None, (err, None))
    # passwords must be > 6 characters but not > 255
    if len(password) < 6 or len(password) > 255:
      err.append('password' + ' ' + 'Range')
      return (None, (err, None))
  #existance check
  except KeyError:
    password = None
    err.append('password' + ' ' + 'None')
    return (None, (err, None))
  
  # check the name
  try:
    name = dictUser['name']
    # name must be a string
    if not isinstance(name, basestring):
      err.append('name' + ' ' + 'Type')
      return (None, (err, None))
    # cannot be longer than 255 characters
    if len(name) > 255:
      err.append('name' + ' ' + 'Range')
      return (None, (err, None))
  # a name can be null
  except KeyError:
    name = None
    
  # check the location
  try:
    location = dictUser['location']
    # location must be a string
    if not isinstance(location, basestring):
      err.append('location' + ' ' + 'Type')
      return (None, (err, None))
    # cannot be longer than 255 characters
    if len(location) > 255:
      err.append('location' + ' ' + 'Range')
      return (None, (err, None))
  # a location can be null
  except KeyError:
    location = None
    
  # check the dateOf Birth
  try:
    dateOfBirth = dictUser['dateOfBirth']
    #print 'Bad Birfday Hurr: ' + dateOfBirth
    # check to see if it's a valid birthdate
    if not isinstance(dateOfBirth,basestring):
      err.append('dateOfBirth' + ' ' + 'Type')
      return (None, (err, None))
    try:
      datetime.datetime.strptime(dateOfBirth, '%Y-%m-%d')
    except ValueError:
      err.append('dateOfBirth' + ' ' + 'Type')
      return (None, (err, None))
    # No Methusalahs allowed
    if int(dateOfBirth[:4]) < 1900:
      err.append('dateOfBirth' + ' ' + 'Range')
      return (None, (err, None))
  # dateOfBirth may be null
  except KeyError:
    dateOfBirth = None
    
  # check the imagePath
  try:
    imagePath = dictUser['imagePath']
    # imagePath must be a string
    if not isinstance(imagePath, basestring):
      err.append('imagePath' + ' ' + 'Type')
      return (None, (err, None))
    # imagePath must be <= 255 characters
    if len(imagePath) > 255:
      err.append('imagePath' + ' ' + 'Range')
      return (None, (err, None))
  # imagePath may be null
  except KeyError:
    imagePath = None

  return (UserInfo(userID, emailAddress, password, name, location, dateOfBirth, imagePath), None)
  
