from __future__ import print_function
from collections import defaultdict
import re
import sys
from time import time
import numpy as np
import operator


from sklearn.feature_extraction.text import TfidfVectorizer

import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from pymongo import MongoClient
import json


client = MongoClient('mongodb://root:Eight123@ds053784.mongolab.com:53784/sccs_scrapeproject')
db = client.sccs_scrapeproject
scrapies = db.scrapies

#Function for clearly printing a dictionary's values
def dictPrint(dictIn):
	for attribute, value in dictIn.items():
		print('{} : {}'.format(attribute, value))
	print('\n')

def getCorpus(cursor):
	for row in cursor:
		rowText = row.get('content', '')
		corpus.append(rowText)

#db.scrapies.find({"time" : { $gte : new ISODate("2010-09-18T20:33:31.000Z") }});
#{u'dataType': u'post', u'contentid': u'358709957509268_774204755959784', u'userid': u'10203038139665439', u'content': u"I have a collection of videos that I'm looking to stream to my tv. They are mp4's and i've looked into stuff like chromecasts but I can't stream those to my tv from my computer/ipad/iphone. Does anyone have any ideas?", u'__v': 0, u'time': datetime.datetime(2014, 9, 18, 20, 33, 31), u'_id': ObjectId('5648f2b6a8255da2cdb7c595')}
#dbCursor = scrapies.find({"$or": [{"dataType": "post"}, {"dataType": "comment"}]})
dbCursor = scrapies.find()
corpus = []
getCorpus(dbCursor)


vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 20, stop_words = 'english', use_idf='True')
X = vectorizer.fit_transform(corpus)
idf = vectorizer.idf_
zipped = dict(zip(vectorizer.get_feature_names(), idf))

sorted_dict = sorted(zipped.items(), key=operator.itemgetter(1), reverse=True)
json.dump(sorted_dict, open("topWords.txt",'w'))

with open("top50words.txt", 'w') as txtFile:
	for x in range(0,50):
		txtFile.write(sorted_dict[x][0] + "\n")


