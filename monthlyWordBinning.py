import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from pymongo import MongoClient
import json
import nltk

client = MongoClient('mongodb://root:Eight123@ds053784.mongolab.com:53784/sccs_scrapeproject')
db = client.sccs_scrapeproject
scrapies = db.mscrapies
dbCursor = scrapies.find()

stopwords = nltk.corpus.stopwords
# stop = stopwords.words('english')
# print stop

#Function for clearly printing a dictionary's values
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


# A function for binning the times of each posts
def monthBinning(cursor):
	for row in cursor:
		rowMonth = row['time'].month
		monthBins[rowMonth] += 1
	dictPrint(monthBins)
	

def getMaxesMonth(wordBin):
	ret = {}
	for year in wordBin:
		ret[year] = {}

		for month in wordBin[year]:
			greatest = -1
			greatestWord = None

			for word in wordBin[year][month]:
				if wordBin[year][month][word] > greatest:
					greatestWord = word
					greatest = wordBin[year][month][word]

			ret[year][month] = {'word': greatestWord, 'frequency' : greatest}

	return ret



def monthlyWordBinning(cursor):
	wordBins = {}

	for row in cursor:
		rowyear = row['time'].year
		rowmonth = row['time'].month	

		if  rowyear not in wordBins:
			wordBins[rowyear] = {}
		if rowmonth not in wordBins[rowyear]:
			wordBins[rowyear][rowmonth] = {}

		if 'content' not in row:
			continue

		tokens = row['content'].split()

		for word in tokens:
			if word in stop:
				continue

			if word not in wordBins[rowyear][rowmonth]:
				wordBins[rowyear][rowmonth][word] = 1
			else:
				wordBins[rowyear][rowmonth][word] = wordBins[rowyear][rowmonth][word] + 1

	# for year in wordBins:
	# 	for month in wordBins[year]:
	# 		for word in wordBins[year][month]:
	# 			# print "{0} : {1}".format(word, wordBins[year][month][word])
	# 			dictPrint(wordBins[year][month])
				# dictPrint(wordBins)
	return wordBins
	

def timeToFirstComment():
	postCursor = scrapies.find({'dataType' : 'post'})
	ret = []
	nocomments = 0

	for post in postCursor:
		# print post
		postid = post['contentid']
		commentCursor = scrapies.find({'references' : postid })

		if commentCursor.count() == 0:
			nocomments += 1
			continue

		quickest = commentCursor[0]
		posttime = post['time']

		for comment in commentCursor:
			if quickest['time'] > comment['time']:
				quickest = comment 

		delta = quickest['time'] - posttime
		print delta
		ret.append(delta)

	print ret

timeToFirstComment()

# monthBins = dict.fromkeys(range(1, 13), 0)
# timeMonths = []
# allMonths = range(1,12)
# monthlyWordBin = monthlyWordBinning(dbCursor)
# monthlyWordFavorites = getMaxesMonth(monthlyWordBin)


# data = [

# 	go.Scatter(
# 		x = allMonths,
# 		y = getVals(monthBins),
# 		marker=dict(
# 	        color='blue',
# 	        line=dict(
# 	            color='grey',
# 	            width=0
# 	        )
# 	    ),
# 	    opacity=0.75
# 	)
# ]

# layout = go.Layout(
#     title='CS Facebook Group Posts Yearly',
#     xaxis=dict(
#         title='Month'
#     ),
#     yaxis=dict(
#         title='# of Posts'
#     ),
#     barmode='overlay',
#     bargap=0.25,
#     bargroupgap=0.3
# )

# fig = go.Figure(data=data, layout=layout)

#plot_url = py.plot(fig, filename='time-line')