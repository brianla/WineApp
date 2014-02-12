import traceback
from RecommendIOController import *

DEBUG = True 

def runRecTests(log, thisUser):
	try:
		#if DEBUG: 
		#	print "About to create a channel"
        	#testInputCreateChannel(log,thisUser)
		#if DEBUG:
		#	print "Created a channel"
        	testInputRemoveChannel(log)
        	testInputAddSeeds(log)
        	testInputRemoveSeeds(log)
       		testInputRecommend(log)
	except:
		ex, ex_type, tb = sys.exc_info()
		print ex
		print ex_type
		traceback.print_tb(tb)
		del tb


def testInputCreateChannel(log,thisUser):
	if DEBUG:
		print "testInputCreateChannel"
        channelName = "My Testing Channel"
        seeds = []
        seeds.append(1)
        seeds.append(4)
        seeds.append(27)
	if DEBUG:
		print "calling inputCreateChannel"
        log.append("Testing the creation of a channel: " +
                   str(inputCreateChannel(thisUser,channelName,seeds)))

def testInputRemoveChannel(log):
	if DEBUG:
		print "testInputRemoveChannel"
        log.append("Removing a channel: " +
                   str(inputRemoveChannel(9)))
                   
def testInputAddSeeds(log):
        seeds = []
        seeds.append(1)
        seeds.append(2)
        seeds.append(3)
        seeds.append(5)
        seeds.append(8)
        log.append("Adding seeds: " +
                   str(inputAddSeeds(10,seeds)))

def testInputRemoveSeeds(log):
        seeds = []
        seeds.append(1)
        seeds.append(2)
        log.append("Removing seeds: " +
                   str(inputRemoveSeeds(10,seeds)))

def testInputRecommend(log):
        log.append("Recommending wines....")
        wines = inputRecommend(31,10)
        log.append("Recommended wines: " +
                   str(wines))
 	for wine in wines:
		log.append("WineID: " + str(wine.wineID) + 
			   ", WineName: " + str(wine.wineName) +
			   ", Winery: " + str(wine.winery) +
			   ", Vintage: " + str(wine.vintage))
