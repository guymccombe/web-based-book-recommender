from flask import Flask, Response, render_template, request, abort, redirect, url_for, session
from os import path
import pandas as pd

app = Flask(__name__)
app.secret_key = "bookRecommenderAssignment"


@app.route("/index.html")
@app.route("/")
def home():
    if "username" in session:
        username = session["username"]
        return render_template("index.html", name=username)
    return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def loginHandler():
    username = request.get_json()["username"]
    if (isUserInDB(username)):
        session["username"] = username
        return redirect(url_for("home"))
    else:
        abort(Response("User not found, if you're new please register.", 404))


def isUserInDB(user):
    return ratings["user_id"].isin([user]).any()


@app.route("/register", methods=['POST'])
def registerHandler():
    username = request.get_json()["username"]
    if (isUserInDB(username)):
        abort(Response("User already exists, try logging in if this is you.", 403))
    else:
        session["username"] = username
        return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    rootPath = path.dirname(__file__)
    ratings = pd.read_csv(path.join(rootPath, "data/ratings.csv"))
    books = pd.read_csv(path.join(rootPath, "data/books.csv"))
    ratings_books = pd.merge(ratings, books, on="book_id")

    app.run(port=8080, debug=True)
