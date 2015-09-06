import unicodedata
from flask import Flask, jsonify, render_template, request, url_for
from pymongo import *
from werkzeug.routing import BaseConverter, ValidationError
from itsdangerous import base64_encode, base64_decode
from bson.objectid import ObjectId
from bson.errors import InvalidId

class ObjectIDConverter(BaseConverter):
    def to_python(self, value):
        try:
            return ObjectId(base64_decode(value))
        except (InvalidId, ValueError, TypeError):
            raise ValidationError()
    def to_url(self, value):
        return base64_encode(value.binary)


app = Flask(__name__)
app.url_map.converters['objectid'] = ObjectIDConverter
cli = MongoClient()
db = cli.finra
cursor = db.dataset.find()
co_names = []
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

for i in cursor:
	if type(i["CrntEmps"]["CrntEmp"]) == type(co_names):
		co_names.append(i["CrntEmps"]["CrntEmp"][0]["@orgNm"])
	else:
		co_names.append(i["CrntEmps"]["CrntEmp"]["@orgNm"])
	co_names = set(co_names)
	co_names = list(co_names)

co_names = [x.encode('UTF8') for x in co_names]

@app.route("/",methods=['POST','GET'])
def index():
	#search_form = SearchForm()
	return render_template("index.html",companies=co_names,states=states) #form=search_form)

@app.route("/search",methods=['POST','GET'])
def search_advisors():
	companies = []
	if request.method == 'POST':
		cursor = db.dataset.find({"CrntEmps.CrntEmp.@orgNm":str(request.form['company'])})
		for i in cursor:
			companies.append(i)
		#cursor = db.dataset.find({"Info.@firstNm":firstname,"Info.@lastNm":lastname})
		# for i in cursor:
		# 	res.append(i)
	return render_template("search_results.html",res=companies)

@app.route("/advisor/<objectid:id>",methods=['POST','GET'])
def view_advisor_detail(id):
	drps = []
	prevous_employment = []
	passed_examinations = []
	other_name = []
	res = []
	cursor = db.dataset.find({"_id":id})
	for i in cursor:
		if i["OthrNms"] != None:
			other_name.append(i["OthrNms"])
		# if i["DPRs"] != None:
		# 	drps.append(i["DPRs"])
		
		res.append(i)

	#get current company
	#get passed examinations
	#get DRP info
	return render_template("advisor_info.html",result=res)

@app.route('/autocomplete',methods=['GET'])
def autocomplete():
	return jsonify(json_list=co_names)


if __name__ == "__main__":
	app.run(debug=True)
