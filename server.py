from flask import Flask, render_template, request
from os import path
import pandas as pd

app = Flask(__name__)

@app.route("/")
def output():
    return render_template("login.html")

@app.route("/login", methods = ['POST'])
def loginHandler():
    username = request.get_json()["username"]
    return username

@app.route("/register", methods = ['POST'])
def registerHandler():
    username = request.get_json()["username"]
    return username

if __name__ == "__main__":
    rootPath = path.dirname(__file__)
    ratings = pd.read_csv(path.join(rootPath, "data/ratings.csv"))
    app.run(port=8080, debug=True)
