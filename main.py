from os import error
from flask import Flask, flash, render_template, request
from hackerearth_scraper import *

mapquery = {
    "webd": ['html', 'flask', 'css', 'bootstrap', 'express', 'script', 'javascript', 'rest', 'django', 'node', 'sql', 'react', 'deploy', 'php', 'server', 'ruby'],
    "sde": ['c++', 'cpp', 'c', 'java', 'script', 'python'],
    "mlai": ['jupyter', 'r', 'machine', 'learn', 'scikit', 'tensor', 'pytorch', 'data', 'cuda'],
    "javad": ['java']
}
def read_data():
    with open('scrapeddata.json', 'r') as f:
        return json.load(f)


def score_queries(data, param):
    scores={} # id, score
    for x in data:
        if 'skills' in data[x]:
            for sk in data[x]['skills']:
                for keyw in param:
                        if keyw in sk.lower():
                            try:
                                scores[x] += 1
                            except KeyError:
                                scores[x] = 1

    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    ranked_data = {}
    for x in scores:
        ranked_data[x[0]] = data[x[0]]
    return ranked_data


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/result", methods=['POST'])
def result():
    recruiter_url = request.form['recruiter']

    if "hackerearth" in recruiter_url:
        scrape_hearth(recruiter_url)
        data = read_data()
        return render_template("out.html", profiles=data)

    error = "Please provide a valid HackerEarth profile link"
    flash(error)
    return render_template("index.html", error=error)


@app.route("/query", methods=['POST'])
def query():
    query_req = request.form['sortby']

    if query_req == 'default':
        return render_template("out.html", profiles=read_data())

    query_data = score_queries(read_data(), mapquery[request.form['sortby']])
    return render_template("out.html", profiles=query_data, sel=query_req)

if __name__ == "__main__":
    # app.secret_key = 'supersecretkey'
    # app.config['SESSION_TYPE'] = 'filesystem'
    # sess.init_app(app)
    app.run(host="127.0.0.1", port=8080, debug=True)