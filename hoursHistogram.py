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

# A function for binning the times of each posts
def timeBinning(cursor):
	count = 0;
	for row in cursor:
		timeHour = row['time'].hour
		times.append(timeHour)
		

times = []
#hourBins = dict.fromkeys(range(0, 24), 0)
timeBinning(dbCursor)


data = [

	go.Histogram(
		x = times,
		marker=dict(
	        color='fuchsia',
	        line=dict(
	            color='grey',
	            width=0
	        )
	    ),
	    opacity=0.75
	)
]

layout = go.Layout(
    title='CS Facebook Group Post Hours',
    xaxis=dict(
        title='Hour'
    ),
    yaxis=dict(
        title='# of Posts'
    ),
    barmode='overlay',
    bargap=0.25,
    bargroupgap=0.3
)

fig = go.Figure(data=data, layout=layout)

plot_url = py.plot(fig, filename='time-histogram')
