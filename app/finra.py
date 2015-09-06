import xmltodict, json
import couchdb
from pymongo import *

mongo = MongoClient("45.55.228.139:27017")
mongodb = mongo.finra

data = open('data.xml')
data = xmltodict.parse(data)
for individual in data['IAPDIndividualReport']['Indvls']['Indvl']:
	mongodb.dataset.insert_one(individual)
# cli = couchdb.Server()
# db = cli['finra']
#save the xml to couch
#retrun id of saved xml
#loop through and save to mongo
#docs = db['3c381ae20cb8003b2ea552696a0009ae']
# for i in docs['finra']['IAPDIndividualReport']['Indvls']['Indvl']:
# 	#SAVE I AS A INDIVIDUAL
# 	mongodb.dataset.insert_one(i)

# for doc in docs.finra:
# 	for do in doc.IAPDIndividualReport:
# 		for d in do.Indvls:
# 			print d
