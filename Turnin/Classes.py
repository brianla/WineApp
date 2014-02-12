
"""All classes used by System. Identical to database table counterparts.
   Check Database Schema for additional details.
"""



DEBUG = True

class UserInfo:
  def __init__(self, 
               userID = None, 
               emailAddress = None, 
               password = None, 
               name = None,
               location = None,
               dateOfBirth = None,
               imagePath = None):

    self.userID = userID
    self.emailAddress = emailAddress
    self.password = password
    self.name = name
    self.location = location
    self.dateOfBirth = dateOfBirth
    self.imagePath = imagePath


class LocationMap:
  def __init__(self,
               locationID = None,
               lm_userID = None,
               locationName = None,
               timeCreated = None,
               imagePath = None):

    self.locationID = locationID
    self.lm_userID = lm_userID
    self.locationName = locationName
    self.timeCreated = timeCreated
    self.imagePath = imagePath


class LocationHistory:
  def __init__(self,
               lh_index = None,
               lh_locationID = None,
               lh_wineID = None,
               timestamp = None,
               eventTag = None):
    self.lh_index = lh_index
    self.lh_locationID = lh_locationID
    self.lh_wineID = lh_wineID
    self.timestamp = timestamp
    self.eventTag = eventTag


class LocationInventory:
  """A wine in the user's inventory
  """
  def __init__(self,
               li_index = None,
               li_locationID = None,
               li_wineID = None,
               quantity = None,
               tags = None,
               description = None,
               imagePath = None,
               personalStarRating = None,
               isWishlist = None,
               bitter = None,
               sweet = None,
               sour = None,
               salty = None,
               chemical = None,
               pungent = None,
               oxidized = None,
               microbiological = None,
               floral = None,
               spicy = None,
               fruity = None,
               vegetative = None,
               nutty = None,
               caramelized = None,
               woody = None,
               earthy = None):

    self.li_index = li_index
    self.li_locationID = li_locationID
    self.li_wineID = li_wineID
    self.quantity = quantity
    self.tags = tags
    self.description = description
    self.imagePath = imagePath
    self.personalStarRating = personalStarRating
    self.isWishlist = isWishlist
    self.bitter = bitter
    self.sweet = sweet
    self.sour = sour
    self.salty = salty
    self.chemical = chemical
    self.pungent = pungent
    self.oxidized = oxidized
    self.microbiological = microbiological
    self.floral = floral
    self.spicy = spicy
    self.fruity = fruity
    self.vegetative = vegetative
    self.nutty = nutty
    self.caramelized = caramelized
    self.woody = woody
    self.earthy = earthy


class Wine:
  """A wine in the global inventory
  """
  def __init__(self,
               wineID = None,
               wineName = None,
               varietal = None,
               winery = None,
               wineType = None,
               vintage = None,
               region = None,
               clusterID = None,
               CSO = None,
               tags = None,
               description = None,
               averageStarRating = None,
               imagePath = None,
               barcode = None,
               bitter = None,
               sweet = None,
               sour = None,
               salty = None,
               chemical = None,
               pungent = None,
               oxidized = None,
               microbiological = None,
               floral = None,
               spicy = None,
               fruity = None,
               vegetative = None,
               nutty = None,
               caramelized = None,
               woody = None,
               earthy = None):

    self.wineID = wineID
    self.wineName = wineName
    self.varietal = varietal
    self.winery = winery
    self.wineType = wineType
    self.vintage = vintage
    self.region = region
    self.clusterID = clusterID
    self.CSO = CSO
    self.tags = tags
    self.description = description
    self.averageStarRating = averageStarRating
    self.imagePath = imagePath
    self.barcode = barcode
    self.bitter = bitter
    self.sweet = sweet
    self.sour = sour
    self.salty = salty
    self.chemical = chemical
    self.pungent = pungent
    self.oxidized = oxidized
    self.microbiological = microbiological
    self.floral = floral
    self.spicy = spicy
    self.fruity = fruity
    self.vegetative = vegetative
    self.nutty = nutty
    self.caramelized = caramelized
    self.woody = woody
    self.earthy = earthy


class Recommender:
  def __init__(self,
               recommenderID = None,
               r_userID = None,
               channelName = None,
               timeCreated = None):

    self.recommenderID = recommenderID
    self.r_userID = r_userID
    self.channelName = channelName
    self.timeCreated = timeCreated


class RecommenderHistory:
  def __init__(self,
               rh_index = None,
               rh_recommenderID = None,
               rh_wineID = None,
               timestamp = None,
               isSeedBottle = None):

    self.rh_index = rh_index
    self.rh_recommenderID = rh_recommenderID
    self.rh_wineID = rh_wineID
    self.timestamp = timestamp
    self.isSeedBottle = isSeedBottle

