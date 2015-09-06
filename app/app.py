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
	co = request.form['company']
	if request.method == 'POST':
		cursor = db.dataset.find({"CrntEmps.CrntEmp.@orgNm":str(request.form['company'])})
		for i in cursor:
			companies.append(i)
		#cursor = db.dataset.find({"Info.@firstNm":firstname,"Info.@lastNm":lastname})
		# for i in cursor:
		# 	res.append(i)
	return render_template("search_results.html",res=companies,co = co)

@app.route("/advisor/<objectid:id>",methods=['POST','GET'])
def view_advisor_detail(id):
	drps = []
	prevous_employment = []
	passed_examinations = []
	other_name = []
	res = []
	has_civil_judc = None
	has_cust_comp = None
	has_bankrupt = None
	has_reg_action = None
	has_judgement = None
	has_investigation = None
	has_termination = None
	has_criminal = None
	has_bond = None
	has_records = None
	cursor = db.dataset.find({"_id":id})
	co = ''
	st = ''
	for i in cursor:
		co = i["CrntEmps"]["CrntEmp"]["@orgNm"]
		st = i["CrntEmps"]["CrntEmp"]["@state"]
		if i["OthrNms"] != None:
			other_name.append(i["OthrNms"])
		if i["DRPs"] != None:
			if i["DRPs"]["DRP"]["@hasCivilJudc"] == "Y":
				has_records=True
				has_civil_judc = True
			if i["DRPs"]["DRP"]["@hasCustComp"] == "Y":
				has_records=True
				has_cust_comp = True
			if i["DRPs"]["DRP"]["@hasBankrupt"] == "Y":
				has_records=True
				has_bankrupt = True
			if i["DRPs"]["DRP"]["@hasRegAction"] == "Y":
				has_records=True
				has_reg_action = True
			if i["DRPs"]["DRP"]["@hasJudgment"] == "Y":
				has_records=True
				has_judgement = True
			if i["DRPs"]["DRP"]["@hasInvstgn"] == "Y":
				has_records=True
				has_investigation = True
			if i["DRPs"]["DRP"]["@hasTermination"] == "Y":
				has_records=True
				has_termination = True
			if i["DRPs"]["DRP"]["@hasCriminal"] == "Y":
				has_records=True
				has_criminal = True
			if i["DRPs"]["DRP"]["@hasBond"] == "Y":
				has_records=True
				has_bond = True
		else:
			has_records = None


		#{u'DRP': {u'@hasCivilJudc': u'N', u'@hasCustComp': u'Y', u'@hasBankrupt': u'N', u'@hasRegAction': u'N', u'@hasJudgment': u'N', u'@hasInvstgn': u'N', u'@hasTermination': u'N', u'@hasCriminal': u'N', u'@hasBond': u'N'}}
		# if i["DRPs"] != None:
		# 	drps.append(i["DRPs"])

		res.append(i)

	#get current company
	#get passed examinations
	#get DRP info
	return render_template("advisor_info.html",result=res,has_civil_judc=has_civil_judc,has_cust_comp=has_cust_comp,has_bankrupt=has_bankrupt,has_reg_action=has_reg_action,has_judgement=has_judgement,has_investigation=has_investigation,has_termination=has_termination,has_criminal=has_criminal,has_bond=has_bond,has_records=has_records, co=co,st=st)

@app.route('/autocomplete',methods=['GET'])
def autocomplete():
	return jsonify(json_list=co_names)


if __name__ == "__main__":
	app.run(debug=True)
