# import some Python dependencies
import urllib2
import json
import datetime
import csv
import time
import re
import pprint

access_token = ''

with open('secrets.csv','rb') as csvfile:
	readr = csv.reader(csvfile, delimiter=',')
	for x in readr:
		print x[0]
		access_token = x[0]

group_id = '358709957509268'

def getFacebookPageLinks(group_id, access_token):
	#construct the URL string
	base = "https://graph.facebook.com/v2.1"
	node = "/"+group_id+"/feed"
	parameters = "?limit=5000&since=13-9-23&until=14-9-23&access_token=%s" % access_token
	url = base +node + parameters
	print 'url:'+ url
	
	#retrieve data
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
    	data = json.loads(response.read())
	datastring = json.dumps(data, indent=4, sort_keys=True)	 

	#Write JSON to file
	filename = 'computerScience1314.json'
	file_ = open(filename, 'w')
	file_.write(datastring)
	file_.close()

		
getFacebookPageLinks(group_id, access_token)

