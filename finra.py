import xmltodict, json
import couchdb

cli = couchdb.Server()
db = cli['finra']
docs = db['3c381ae20cb8003b2ea552696a0009ae']
for i in docs['finra']['IAPDIndividualReport']['Indvls']['Indvl']:
	print i

# for doc in docs.finra:
# 	for do in doc.IAPDIndividualReport:
# 		for d in do.Indvls:
# 			print d
