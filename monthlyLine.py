import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from pymongo import MongoClient
import json

client = MongoClient('mongodb://root:Eight123@ds053784.mongolab.com:53784/sccs_scrapeproject')
db = client.sccs_scrapeproject
scrapies = db.scrapies

#db.scrapies.find({"time" : { $gte : new ISODate("2010-09-18T20:33:31.000Z") }});
dbCursor = scrapies.find()

#Function for clearly printing a dictionary's values
def dictPrint(dictIn):
	for attribute, value in dictIn.items():
		print('{} : {}'.format(attribute, value))
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

monthBins = dict.fromkeys(range(1, 13), 0)
timeMonths = []
allMonths = range(1,12)
monthBinning(dbCursor)


data = [

	go.Scatter(
		x = allMonths,
		y = getVals(monthBins),
		marker=dict(
	        color='blue',
	        line=dict(
	            color='grey',
	            width=0
	        )
	    ),
	    opacity=0.75
	)
]

layout = go.Layout(
    title='CS Facebook Group Posts Yearly',
    xaxis=dict(
        title='Month'
    ),
    yaxis=dict(
        title='# of Posts'
    ),
    barmode='overlay',
    bargap=0.25,
    bargroupgap=0.3
)

fig = go.Figure(data=data, layout=layout)

#plot_url = py.plot(fig, filename='time-line')