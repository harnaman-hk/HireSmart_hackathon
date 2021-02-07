from flask import Flask, render_template, request
from hackerearth_scraper import *

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/result", methods=['POST'])
def result():
    recruiter_url = request.form['recruiter']

    if "hackerearth" in recruiter_url:
        scrape_hearth(recruiter_url)

    return render_template("out.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)