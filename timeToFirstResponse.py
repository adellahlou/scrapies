import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from pymongo import MongoClient
import json
import pickle
from scipy import stats



# client = MongoClient('mongodb://root:Eight123@ds053784.mongolab.com:53784/sccs_scrapeproject')
# db = client.sccs_scrapeproject
# scrapies = db.mscrapies

# #Function for clearly printing a dictionary's values
# def dictPrint(dictIn):
# 	for attribute, value in dictIn.items():

# 		try:
# 			print('{} : {}'.format(attribute, value))
# 		except Exception as e:
# 			continue

# 	print('\n')


# def getVals(dictIn):
# 	vals = []
# 	for attribute, value in dictIn.items():
# 		vals.append(value)
# 	print(sum(vals))
# 	return vals

	

# def timeToFirstComment():
# 	postCursor = scrapies.find({'dataType' : 'post'})
# 	ret = []
# 	nocomments = 0

# 	for post in postCursor:
# 		# print post
# 		postid = post['contentid']
# 		commentCursor = scrapies.find({'references' : postid })

# 		if commentCursor.count() == 0:
# 			nocomments += 1
# 			continue

# 		quickest = commentCursor[0]
# 		posttime = post['time']

# 		for comment in commentCursor:
# 			if quickest['time'] > comment['time']:
# 				quickest = comment 

# 		delta = quickest['time'] - posttime
# 		print delta
# 		ret.append(delta)

# 	return ret

# deltas = timeToFirstComment()
# average = deltas[0]
# for delta in deltas:
# 	average += delta
# average -= deltas[0]
# print average
# print len(deltas)
# average = average / len(deltas)
# print average

# pickle.dump(deltas, open("timeToFirstResponse.pickle", "wb"))

# monthBins = dict.fromkeys(range(1, 13), 0)
# timeMonths = []
# allMonths = range(1,12)
# monthlyWordBin = monthlyWordBinning(dbCursor)
# monthlyWordFavorites = getMaxesMonth(monthlyWordBin)


def describeResults():
	deltas = pickle.load(open('timeToFirstResponse.pickle', 'rb'))
	changed = [delta.total_seconds() for delta in deltas ]
	top = []
	cutoff = changed[0]
	for change in changed:
		if len(top) < 100:
			top.append(change)
			cutoff = change if change < cutoff else cutoff
		else:
			if change > cutoff:
				top.remove(cutoff)
				top.append(change)
				cutoff = change

	description = stats.describe(changed)
	description2 = stats.describe(top)
	print description
	print description2

describeResults()
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