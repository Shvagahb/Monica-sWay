import xmltodict, json


data = open('data.xml')
print xmltodict.parse(data)
