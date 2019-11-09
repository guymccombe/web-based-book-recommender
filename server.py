from flask import Flask, render_template, request
from os import path
import pandas as pd

app = Flask(__name__)

@app.route("/")
def output():
    return render_template("index.html")

@app.route("/login", methods = ['POST'])
def loginHandler():
    data = request.get_json()
    print(data)
    return "OK"

if __name__ == "__main__":
    rootPath = path.dirname(__file__)
#    ratings = pd.read_csv(path.join(rootPath, "data/ratings.csv"))
    app.run(port=8080, debug=True)
