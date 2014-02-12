from xml.sax import saxutils

##########################################################################################
# XML feature is postponed for future development
##########################################################################################


class XMLLocation:
  def __init__(self)
    self.wines = []
    self.locationID = None
    

class XMLParser(saxutils.DefaultHandler):
  def __init__(self)
    self.locations = []
    self.currLocation = None
    self.currInventoryItem = None
    self.username = None
    #That is just a LocationInventory object
    
    
  def startElement(self, name, attrs):
    if name == "Inventory"
      self.username = attrs.get('Name', None)
    else if name == "Location"
      currLocation = XMLLocation()
      currLocation.locationID = attrs.get('Location', None)
    else
      self.currInventoryItem = LocationInventory()
      self.currInventoryItem.li_wineID = attrs.get('li_wineID', None)
      #self.currInventoryItem.li_locationID = attrs.get('li_locationID', None)
      self.currInventoryItem.personalStarRating = attrs.get('personalStarRating', None)
      self.currInventoryItem.isWishList = attrs.get('isWishList', None)
      self.currInventoryItem.bitter = attrs.get('bitter', None)
      self.currInventoryItem.sweet = attrs.get('sweet', None)
      self.currInventoryItem.sour = attrs.get('sour', None)
      self.currInventoryItem.salty = attrs.get('salty', None)
      self.currInventoryItem.chemical = attrs.get('chemical', None)
      self.currInventoryItem.pungent = attrs.get('pungent', None)
      self.currInventoryItem.oxidized = attrs.get('oxidized', None)
      self.currInventoryItem.microbiological = attrs.get('microbiological', None)
      self.currInventoryItem.floral = attrs.get('floral', None)
      self.currInventoryItem.spicy = attrs.get('spicy', None)
      self.currInventoryItem.vegetative = attrs.get('vegetative', None)
      self.currInventoryItem.nutty = attrs.get('nutty', None)
      self.currInventoryItem.carmelized = attrs.get('carmelized', None)
      self.currInventoryItem.woody = attrs.get('woody', None)
      self.currInventoryItem.eathy = attrs.get('eathy', None)
      
    def endElement(self, name):
      if name == Inventory
      
      else if name == Location
        self.locations.append(currLocation)
        currLocation = None
      else
        currLocation.wines.append(currInventoryItem)
        currInventoryItem = None
