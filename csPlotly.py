import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from pymongo import MongoClient
import json

client = MongoClient('mongodb://root:Eight123@ds053784.mongolab.com:53784/sccs_scrapeproject')
db = client.scrapies
scrapies = db.scrapies

#db.scrapies.find({"time" : { $gte : new ISODate("2010-09-18T20:33:31.000Z") }});
dbCursor = scrapies.find()
print(dbCursor)

postTimes = []
commentTimes = []

def timeBinning(cursor):
	count = 0;
	for row in cursor:
		count = count + 1
		if(count < 10):
			print row
		else:
			break


timeBinning(dbCursor)

# def getData(filename):
# 	with open(filename) as json_data:    
# 		data = json.load(json_data)
# 		nodes = data["nodes"];

# 		for obj in nodes:
# 			if(obj["dataType"] == 'post'):
# 				postTimes.append(obj["time"])

# 			if(obj["dataType"] == 'comment'):
# 				commentTimes.append(obj["time"])


# getData('test.txt');

#print(postTimes)
#print(commentTimes)

data = [

	go.Scatter(
		x = postTimes, 	#x=['2014-8-04 22:23:00', '2014-12-04 22:23:00', '2015-6-04 22:23:00'],
	    y = postTimes
	)
]

plot_url = py.plot(data, filename='date-axes')