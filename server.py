from flask import Flask, Response, render_template, request, abort, redirect, url_for, session, jsonify
from os import path
from numpy import mean, diag, dot
from scipy.sparse.linalg import svds
import pandas as pd

from recommendations import Recommendations

app = Flask(__name__)
app.secret_key = "bookRecommenderAssignment"


@app.route("/index.html")
@app.route("/")
def home():
    if "username" in session:
        username = session["username"]
        return render_template("index.html", name=username)
    return redirect(url_for("login"))


@app.route("/recommend", methods=["GET"])
def recommend():
    if "username" in session:
        user = userNameToID(session["username"])
        return jsonify(recommender.getRecommendations(user))
    else:
        abort(403)


def userNameToID(username):
    # TODO permanent solution instead of casting username to int
    return int(username)


@app.route("/rating", methods=["POST"])
def rate():
    if "username" not in session:
        return redirect(url_for("login"))
    else:
        addRating(*request.form.values())
        return redirect(url_for("home"))


def addRating(title, rating, genre):
    # TODO Post rating
    print()


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def loginHandler():
    username = request.get_json()["username"]
    if (recommender.isUserInDB(username)):
        session["username"] = username
        return redirect(url_for("home"))
    else:
        abort(Response("User not found, if you're new please register.", 404))


@app.route("/register", methods=['POST'])
def registerHandler():
    username = request.get_json()["username"]
    if (recommender.isUserInDB(username)):
        abort(Response("User already exists, try logging in if this is you.", 403))
    else:
        session["username"] = username
        return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    recommender = Recommendations()
    app.run(port=8080, debug=True)
