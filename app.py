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


@app.route("/",methods=['POST','GET'])
def index():
	#search_form = SearchForm()
	co_names = []
	states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
	cursor = db.dataset.find()
	for i in cursor:
		if type(i["CrntEmps"]["CrntEmp"]) == type(co_names):
			co_names.append(i["CrntEmps"]["CrntEmp"][0]["@orgNm"])
		else:
			co_names.append(i["CrntEmps"]["CrntEmp"]["@orgNm"])
	# co_names_unique = []
	# co_names_unique = [i for i in co_names if i not in co_names_unique]
	# print co_names_unique
	co_names = set(co_names)
	co_names = list(co_names)
	co_names.sort()
	return render_template("index.html",companies=co_names,states=states) #form=search_form)

@app.route("/search",methods=['POST','GET'])
def search_advisors():
	res = []
	if request.method == 'POST':
		firstname = str(request.form['firstname']).upper()
		lastname = str(request.form['lastname']).upper()
		cursor = db.dataset.find({"Info.@firstNm":firstname,"Info.@lastNm":lastname})
		for i in cursor:
			res.append(i)
	return render_template("search_results.html",res=res)

@app.route("/advisor/<objectid:id>",methods=['POST','GET'])
def view_advisor_detail(id):
	cursor = db.dataset.find({"CrntEmps.CrntEmp.@orgNm"})
	for i in cursor:
		print i
	return render_template("advisor_info.html")


if __name__ == "__main__":
	app.run(debug=True)
