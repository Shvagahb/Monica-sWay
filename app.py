import couchdb
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/search")
def search_advisors():
	return render_template("search_results.html")

@app.route("/advisor/")
def view_advisor_detail():
	return render_template("advisor_info.html")


if __name__ == "__main__":
	app.run(debug=True)
