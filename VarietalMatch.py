"""Module for finding closest matching varietal to a user given one.
"""

import re

# On import, retrieve, parse, and store the list of known varietals
varietals_file = open('WineList.txt', 'r')
global_varietals = varietals_file.read()
varietals_file.close()

global_varietals = global_varietals.strip()
global_varietals = global_varietals.split('\n')


for i in range(len(global_varietals)):
	# remove extension
	global_varietals[i] = re.sub('\..*', '', global_varietals[i])


def getScore(string1, string2):
	"""Implementation of character pattern matching

	Do character matching between user_varietal and every varietal in
	global_varietals. Assign 1 point for every match of one char, 2 for
	two chars in a row, 4 for three chars in a row, 8 for four, etc.

	Args:
		string string1: First string
		string string2: Second string

	Return:
		int: The score of this comparison
	"""
	string1 = string1.lower()
	string2 = string2.lower()

	length1 = len(string1)
	length2 = len(string2)
	score = 0
	
	# Use each char in string1 as starting point
	for i in range(length1):
		index = i
		matchLength = 0

		for j in range(length2):
			if string1[index] == string2[j]:
				matchLength += 1
				index += 1

				if index >= length1 or j == length2 - 1:
					score += pow(2, matchLength - 1)
					index = i
					matchLength = 0

			else:
				if 0 < matchLength:
					score += pow(2, matchLength - 1)

				matchLength = 0
				index = i
				matchLength = 0

	score /= float(len(string2))

	return score



def findVarietalMatch(user_varietal):
	"""Find the closest varietal to user_varietal in global_varietals.

	Do character matching between user_varietal and every varietal in
	global_varietals. Assign 1 point for every match of one char, 2 for
	two chars in a row, 4 for three chars in a row, 8 for four, etc.

	Arg:
		string user_varietal: The user-given varietal name

	Return:
		string: The name of the matching varietal
	"""
	match = ''
	max_score = 0
	user_varietal = user_varietal.lower()

	for global_varietal in global_varietals:
		curr_score = getScore(user_varietal, global_varietal)
		if max_score < curr_score:
			max_score = curr_score
			match = global_varietal

	return match