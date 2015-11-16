import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from pymongo import MongoClient
import json
import pickle
from scipy import stats



client = MongoClient('mongodb://root:Eight123@ds053784.mongolab.com:53784/sccs_scrapeproject')
db = client.sccs_scrapeproject
scrapies = db.mscrapies
dbCursor = scrapies.find()

# #Function for clearly printing a dictionary's values
def dictPrint(dictIn):
	for attribute, value in dictIn.items():

		try:
			print('{} : {}'.format(attribute, value))
		except Exception as e:
			continue

	print('\n')


def getVals(dictIn):
	vals = []
	for attribute, value in dictIn.items():
		vals.append(value)
	print(sum(vals))
	return vals


def getUserData(cursor):
	users = {}

	for post in cursor:
		userid = post['userid']
		dtype = post['dataType']

		if userid not in users:
			users[userid] = {'post' : 0, 'comment' : 0, 'userid': userid}

		users[userid][dtype] = users[userid][dtype] + 1

	return users

def userMin(data, attribute):
	miniVal = data[0][attribute]
	miniUser = data[0]

	for user in data:
		if user[attribute] < miniVal:
			miniVal = user[attribute]
			miniUser = user

	return miniUser


def topPosters(data):
	top = []
	curData = data

	for i in range(10):
		maxi = -1
		maxiUserKey = None

		for userkey in curData:
			user = curData[userkey]

			if user['post'] > maxi:
				maxi = user['post']
				maxiUserKey = userkey

		top.append(curData[maxiUserKey])
		del curData[maxiUserKey]

	return top

def topCommenters(data):
	top = []
	curData = data
	key = 'comment'

	for i in range(10):
		maxi = -1
		maxiUserKey = None

		for userkey in curData:
			user = curData[userkey]

			if user[key] > maxi:
				maxi = user[key]
				maxiUserKey = userkey

		top.append(curData[maxiUserKey])
		del curData[maxiUserKey]

	return top


userData = getUserData(dbCursor)
print topPosters(userData)
print topCommenters(userData)


# pickle.dump(deltas, open("timeToFirstResponse.pickle", "wb"))
# monthBins = dict.fromkeys(range(1, 13), 0)
# timeMonths = []
# allMonths = range(1,12)
# monthlyWordBin = monthlyWordBinning(dbCursor)
# monthlyWordFavorites = getMaxesMonth(monthlyWordBin)


# def describeResults():
# 	deltas = pickle.load(open('timeToFirstResponse.pickle', 'rb'))
# 	changed = [delta.total_seconds() for delta in deltas ]
# 	top = []
# 	cutoff = changed[0]
# 	for change in changed:
# 		if len(top) < 100:
# 			top.append(change)
# 			cutoff = change if change < cutoff else cutoff
# 		else:
# 			if change > cutoff:
# 				top.remove(cutoff)
# 				top.append(change)
# 				cutoff = change

# 	description = stats.describe(changed)
# 	description2 = stats.describe(top)
# 	print description
# 	print description2

# describeResults()
# data = [
