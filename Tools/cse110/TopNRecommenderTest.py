from math import floor
from random import random

class TopNRecommenterTest:
    vectorFile = open("WIneVectors_CSV.csv")
    n_TopRecommended = 5
    k_RandomWines = 10
    c_typeScalar = 0.1
    c_varietalScalar = 0.1

    DEBUG = False

    def run():
        print ("Loading Wine Vector Data")
        # open the csv file
        reader = csv.reader(vectorFile, 'rb')
        print ("Running Test: Retrieving Top-" + str(n_TopRecommended) + " wines for "
        + str(k_RandomWines) + " random wines.")
        runTest1(data)

###################### Calculation Methods ############################

    def runTest1(reader):
        # Make a integer hash set called randomIndicies, populate with getRandomK(
        
        
        #row = None
        #no loop, one wine
        row = data.getRows()# get rows; get i from the csv file
        pairs = generatePairs(data, row_i, i)
        print("Wine: " + row_i.getValueByKey(Keys.id)
                + "," + row_i.getValueByKey(Key.wineName)
                + "," + row_i.getValueByKey(Keys.winery))

        print("Top-" + n_TopRecommended + ": ")
        for j in n_TopRecommended:
            print("\tWine: " + col("Dist: " + pairs.get(j).second, 15)
                    + " Vector: " + pairs.get(j).first.getValueByKey(Keys.id)
                    + ", " + pairs.get(j).first.getValueByKey(Keys.winename)
                    + ", " + pairs.get(j).first.getValueByKey(Keys.winery))
    
        print("\n")
        
        
        

	def generatePairs(data, row_i, i):
		pairs = list()
		row = None
		dist = -1.0
		pair = None
		for r in range(0, data.getRows().size()):
		
			if i == r:
				continue
			row = data.getRows().get(r)
			dist = getSquaredDistance(row_i, row)
			pair = row, dist
			pairs.append(pair)
		
		return pairs
		
	def getRandom(min, max, k):

		ints = dict()
		k -= 1
		while k >= 0:
			ints.update(  math.floor(min + (max-min)*random.random())  )
			k -= 1
		return ints
		
        # Having trouble with this one
	def getSquaredDistance(row_i, row):
		dist = 0.0
		for(key in Keys.aroma)
			dist += math.pow(  (double(row_i.getValueByKey(key)) - double(row.getValueByKey(key)))  , 2.0)
		dist += 0 if (wineType(row_i) == (wineType(row))) else c_typeScalar
		dist += 0 if (wineVarietal(row_i) == (wineVarietal(row))) else c_varietalScalar
		return dist
	
	def wineType(row):
		return (row.getValueByKey(Keys.type).lower.strip)
		
	def wineVarietal(row):
		return (row.getValueByKey(Keys.varietal).lower.strip)
		

###################### Helper Methods ##################################


    def col(str, width):
        """ Forces a string to be of length width.

        Truncates the string it is too long. Pads the end of the string
        with " " if it is too short. Returns the resultant string

        Args:
            string str
            int width

        Return:
            string
        """
        # String fixedStr
        fixedStr = None
        # if the string passed in is longer than width truncate it
        if len(str) > width:
            fixedStr = str[0:width]
        #otherwise pad it will spaces so that it is of length width
        else:
            diff = width - len(str)
            fixedStr = str
            for i in range(0, diff):
                fixedStr = fixedStr + " "
        return fixedStr

    def getSortedDistances(rows):
        """

        Args:
            list rows - a list of tuples of the type (CSVRow, double)

        Return:
            list - a list of tuples of type (CSVRow, double)
        """
        sortedList = None
        current = None
        for i in range(0, len(rows)):
            current = rows[i]
            for j in range(len(sortedList), 0, -1):
                if j != 0 and current[1] < sortedList[j-1][1]:
                    continue
                if j == len(sortedList):
                    sortedList.append(current)
                else:
                    sortedList.append(j, current)
                    break
        return sortedList

##################### Private Classes ###################

# no need for a pair class if we have tuples in python

class Keys:

    attributes = None
    # Change add to appends
    aroma = None
    attributes.append("wineID")
    attributes.append("winery")
    attributes.append("wineID")
	attributes.append("winery")
	attributes.append("wineName")
	attributes.append("ava")
	attributes.append("vintage")
	attributes.append("price")
	attributes.append("rating")
	attributes.append("notes")
	attributes.append("region")
	attributes.append("type")
	attributes.append("varietal")
    #aromas are added to two different lists
    attributes.append("bitter")
    attributes.append("sweet")
    attributes.append("sour")
    attributes.append("salty")
    attributes.append("chemical")
    attributes.append("pungent")
    attributes.append("oxidized")
    attributes.append("microbiological")
    attributes.append("floral")
    attributes.append("spicy")
    attributes.append("fruity")
    attributes.append("vegetative")
    attributes.append("nutty")
    attributes.append("caramelized")
    attributes.append("woody")
    attributes.append("earthy")

    aroma.append("bitter")
	aroma.append("sweet")
	aroma.append("sour")
	aroma.append("salty")
	aroma.append("chemical")
	aroma.append("pungent")
	aroma.append("oxidized")
	aroma.append("microbiological")
	aroma.append("floral")
	aroma.append("spicy")
	aroma.append("fruity")
	aroma.append("vegetative")
	aroma.append("nutty")
	aroma.append("caramelized")
	aroma.append("woody")
	aroma.append("earthy")
	
###################### Main ##################################   

def main():
	test = TopNRecommenderTest()
	print("Main(): Begin running Top-N Recommender Test...")
	test.run()
	print("Main(): Finished running Top-N Recommender Test.")

if __name__ == "__main__":
	main()
    
        

    

    
