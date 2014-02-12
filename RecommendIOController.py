"""Recommender system IO module
"""

from flask import *
from Classes import *
from InstantiationValidation import *
import Globals
from RecommendController import *

def inputGetUserShelves(user):
  """returns the list of recommender objects a user owns"""
  return getUserShelves(user)

def inputGetSeeds(recommenderID):
  return getSeeds(recommenderID)

def inputCreateChannel(user, channelName, seeds):
  """Preprocess creating a recommendation channel
  
  Arg:
    UserInfo user: UserInfo object representing the user
    string channelName: The name of the channel
    list seeds: List of wineIDs
  """
  err = []

  if channelName == None:
    err.append('channelName' + ' ' + 'None')
    return (None, (err,None))
  # Check that the channelName is a string
  if not isinstance( channelName, basestring):
    err.append('channelName' + ' ' + 'Type')
    return (None, (err,None))
  # Check that the channelName is shorter than 255 characters
  if len(channelName) > 255:
    err.append('channelName' + ' ' + 'Range')
    return (None, (err,None))

  return createChannel(user, channelName, seeds)
  

def inputEditChannel(recommenderID, channelName):
  """Preprocess changing the name of a channel.

  Arg:
    int recommenderID: ID of the recommender 
    string channelName: Name to change to
  """
  rec = getRecommender(recommenderID)
  if rec[0] == None:
    return rec

  return editChannel(rec, channelName)


def inputRemoveChannel(recommenderID):
  """Preprocess removing a recommendation channel
  
  Arg:
    int recommenderID: The id of the channel.
  """
  err = []

  validateID(recommenderID,err)
  
  if not err:
    return removeChannel(recommenderID)
  else:
    return (None, (err,None))
  
  
def inputAddSeeds(recommenderID, seeds):
  """Preprocess adding seeds to a channel.
  
  Args:
    int recommenderID: The id of the channel
    list seeds: A list of wineIDs specifying seed wines.
  """
  err = []

  validateID(recommenderID,err)

  if not err:
    return addSeeds(recommenderID, seeds)
  else:
    return (None, (err,None))
  
  
def inputRemoveSeeds(recommenderID, seeds):
  """Preprocess removing seeds from a channel.
  
  Args:
    int recommenderID: The id of the channel
    list seeds: A list of wineIDs to remove as seeds.
  """
  err = []

  validateID(recommenderID, err)

  if not err:
    return removeSeeds(recommenderID, seeds)
  else:
    return (None, (err,None))



def inputRecommend(recommenderID, numOfWines):
  """Preprocess recommendation of wines to user
  """ 
  err = []
  print "Validating recommend"
  validateID(recommenderID, err)
  validateCount(numOfWines,err)
  print "Recommend validated"

  if not err:
    return recommend(recommenderID, numOfWines)
  else:
    return (None, (err,None))





def inputGetRecommendHistory(recommenderID):
  """Preprocess retrieval of some number of wines recommended in the past.

  Args:
    int recommenderID: ID of the recommender to get history from
    int numWines: Number of wines from history to return

  Return:
    list of wines
  """
  err = []
  validateID(recommenderID,err)

  if len(err) > 0:
    return (None, (err, None))

  return getRecommendHistory(recommenderID)

  
def inputRandomWines(numWines):
  """Preprocess retrieval of a random set of wines
  """
  err = []
  validateCount(numWines,err)
  
  if len(err) > 0:
    return (None, (err, None))
  return randomWine(numWines)


def inputGetCandidateWines(attrs):
  """ Returns a list of candiate wines for the add shelf modal """

  err = []

  validateAttr(attrs,err)

  if not err:
    return getCandidateWines(attrs)
  else:
    return (None, (err,None))


def validateAttr(attributes,err):
  
  # Check the bitter attribute
  try:
    bitter = attributes['bitter']
    # Check that bitter is a float
    if not isinstance(bitter, float):
      err.append('bitter' + ' ' + 'Type')
    # bitter may not be negative
    if bitter < 0:
      err.append('bitter' + ' ' + 'Range')
  # Check that bitter exists.
  # bitter may be null.
  except KeyError:
    pass
    
  # Check the sweet attribute
  try:
    sweet = attributes['sweet']
    # Check that sweet is a float
    if not isinstance(sweet, float):
      err.append('sweet' + ' ' + 'Type')
    # sweet may not be negative
    if sweet < 0:
      err.append('sweet' + ' ' + 'Range')
  # Check that sweet exists.
  # sweet may be null.
  except KeyError:
    pass
    
  # Check the sour attribute
  try:
    sour = attributes['sour']
    # Check that sour is a float
    if not isinstance(sour, float):
      err.append('sour' + ' ' + 'Type')
    # sour may not be negative
    if sour < 0:
      err.append('sour' + ' ' + 'Range')
  # Check that sour exists.
  # sour may be null.
  except KeyError:
    pass
    
  # Check the salty attribute
  try:
    salty = attributes['salty']
    # Check that salty is a float
    if not isinstance(salty, float):
      err.append('salty' + ' ' + 'Type')
    # salty may not be negative
    if salty < 0:
      err.append('salty' + ' ' + 'Range')
  # Check that salty exists.
  # salty may be null.
  except KeyError:
    pass
    
  # Check the chemical attribute
  try:
    chemical = attributes['chemical']
    # Check that chemical is a float
    if not isinstance(chemical, float):
      err.append('chemical' + ' ' + 'Type')
    # chemical may not be negative
    if chemical < 0:
      err.append('chemical' + ' ' + 'Range')
  # Check that chemical exists.
  # chemical may be null.
  except KeyError:
    pass
    
  # Check the pungent attribute
  try:
    pungent = attributes['pungent']
    # Check that pungent is a float
    if not isinstance(pungent, float):
      err.append('pungent' + ' ' + 'Type')
    # pungent may not be negative
    if pungent < 0:
      err.append('pungent' + ' ' + 'Range')
  # Check that pungent exists.
  # pungent may be null.
  except KeyError:
    pass
    
  # Check the oxidized attribute
  try:
    oxidized = attributes['oxidized']
    # Check that oxidized is a float
    if not isinstance(oxidized, float):
      err.append('oxidized' + ' ' + 'Type')
    # oxidized may not be negative
    if oxidized < 0:
      err.append('oxidized' + ' ' + 'Range')
  # Check that oxidized exists.
  # oxidized may be null.
  except KeyError:
    pass
    
  # Check the microbiological attribute
  try:
    microbiological = attributes['microbiological']
    # Check that microbiological is a float
    if not isinstance(microbiological, float):
      err.append('microbiological' + ' ' + 'Type')
    # microbiological may not be negative
    if microbiological < 0:
      err.append('microbiological' + ' ' + 'Range')
  # Check that microbiological exists.
  # microbiological may be null.
  except KeyError:
    pass
    
  # Check the floral attribute
  try:
    floral = attributes['floral']
    # Check that floral is a float
    if not isinstance(floral, float):
      err.append('floral' + ' ' + 'Type')
    # floral may not be negative
    if floral < 0:
      err.append('floral' + ' ' + 'Range')
  # Check that floral exists.
  # floral may be null.
  except KeyError:
    pass
    
  # Check the spicy attribute
  try:
    spicy = attributes['spicy']
    # Check that spicy is a float
    if not isinstance(spicy, float):
      err.append('spicy' + ' ' + 'Type')
    # spicy may not be negative
    if spicy < 0:
      err.append('spicy' + ' ' + 'Range')
  # Check that spicy exists.
  # spicy may be null.
  except KeyError:
    pass
    
  # Check the fruity attribute
  try:
    fruity = attributes['fruity']
    # Check that fruity is a float
    if not isinstance(fruity, float):
      err.append('fruity' + ' ' + 'Type')
    # fruity may not be negative
    if fruity < 0:
      err.append('fruity' + ' ' + 'Range')
  # Check that fruity exists.
  # fruity may be null.
  except KeyError:
    pass
    
  # Check the vegetative attribute
  try:
    vegetative = attributes['vegetative']
    # Check that vegetative is a float
    if not isinstance(vegetative, float):
      err.append('vegetative' + ' ' + 'Type')
    # vegetative may not be negative
    if vegetative < 0:
      err.append('vegetative' + ' ' + 'Range')
  # Check that vegetative exists.
  # vegetative may be null.
  except KeyError:
    pass
    
  # Check the nutty attribute
  try:
    nutty = attributes['nutty']
    # Check that nutty is a float
    if not isinstance(nutty, float):
      err.append('nutty' + ' ' + 'Type')
    # nutty may not be negative
    if nutty < 0:
      err.append('nutty' + ' ' + 'Range')
  # Check that nutty exists.
  # nutty may be null.
  except KeyError:
    pass
    
  # Check the caramelized attribute
  try:
    caramelized = attributes['caramelized']
    # Check that caramelized is a float
    if not isinstance(caramelized, float):
      err.append('caramelized' + ' ' + 'Type')
    # caramelized may not be negative
    if caramelized < 0:
      err.append('caramelized' + ' ' + 'Range')
  # Check that caramelized exists.
  # caramelized may be null.
  except KeyError:
    pass
    
  # Check the woody attribute
  try:
    woody = attributes['woody']
    # Check that woody is a float
    if not isinstance(woody, float):
      err.append('woody' + ' ' + 'Type')
    # woody may not be negative
    if woody < 0:
      err.append('woody' + ' ' + 'Range')
  # Check that woody exists.
  # woody may be null.
  except KeyError:
    pass
    
  # Check the earthy attribute
  try:
    earthy = attributes['earthy']
    # Check that earthy is a float
    if not isinstance(earthy, float):
      err.append('earthy' + ' ' + 'Type')
    # earthy may not be negative
    if earthy < 0:
      err.append('earthy' + ' ' + 'Range')
  # Check that earthy exists.
  # earthy may be null.
  except KeyError:
    pass

