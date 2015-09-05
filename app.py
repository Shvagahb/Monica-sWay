import couchdb
from flask import Flask, jsonify, render_template
from forms import SearchForm

app = Flask(__name__)
app.secret_key = "MonicaInvestigates"

@app.route("/")
def index():
	search_form = SearchForm()
	return render_template("index.html", form=search_form)

@app.route("/search")
def search_advisors():
	return render_template("search_results.html")

@app.route("/advisor/")
def view_advisor_detail():
	return render_template("advisor_info.html")


if __name__ == "__main__":
	app.run(debug=True)
