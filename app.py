from flask import Flask, jsonify, render_template, request, url_for
from pymongo import *

app = Flask(__name__)
cli = MongoClient()
db = cli.finra

@app.route("/",methods=['POST','GET'])
def index():
	return render_template("index.html")

@app.route("/search",methods=['POST','GET'])
def search_advisors():
	res = []
	if request.method == 'POST':
		firstname = str(request.form['firstname'])
		lastname = str(request.form['lastname'])
		print firstname, lastname
		cursor = db.dataset.find({"Info.@firstNm":firstname,"Info.@lastNm":lastname})
		for i in cursor:
			res.append(i)
	return render_template("search_results.html",res=res)

@app.route("/advisor/")
def view_advisor_detail():
	return render_template("advisor_info.html")


if __name__ == "__main__":
	app.run(debug=True)
