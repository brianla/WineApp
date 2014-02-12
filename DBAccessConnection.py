from flask import *
from Classes import *
import Globals
from sqlalchemy import *
import random
import sys
import datetime
import traceback

#Import database connection config file
import dbConfig

engine = create_engine(dbConfig.DB_URI)
metadata = MetaData(bind=engine)
userInfo = Table('UserInfo', metadata, autoload = True)
locationHistory = Table('LocationHistory', metadata, autoload = True)
locationInventory = Table('LocationInventory', metadata, autoload = True)
locationMap = Table('LocationMap', metadata, autoload = True)
recommenderHistory = Table('RecommenderHistory', metadata, autoload = True)
recommenders = Table('Recommenders', metadata, autoload = True)
wines = Table('Wines', metadata, autoload = True)

con = engine.connect()