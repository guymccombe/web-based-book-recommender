from flask import Flask, Response, render_template, request, abort, redirect, url_for, session
from os import path
from numpy import mean, diag, dot
from scipy.sparse.linalg import svds
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


@app.route("/recommend", methods=["GET"])
def getRecommendations():
    if "username" in session:
        sortedPredicitons = predicitionsDF.iloc[int(session["username"])].sort_values(
            ascending=False)  # TODO permanent solution instead of casting username to int
    else:
        abort(403)


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


def generatePredictionsDFBySingularValueDecomposition(dataframe):
    matrix = dataframe.values
    user_ratings_mean = mean(matrix, axis=1).reshape(-1, 1)
    demeanedMatrix = matrix - user_ratings_mean
    del matrix

    userFeaturesMatrix, weights, bookFeaturesMatrix = svds(
        demeanedMatrix, k=50)
    del demeanedMatrix
    weights = diag(weights)

    userPredictionRatings = dot(
        dot(userFeaturesMatrix, weights), bookFeaturesMatrix) + user_ratings_mean
    predicitions = pd.DataFrame(
        userPredictionRatings, columns=dataframe.columns)

    return predicitions


if __name__ == "__main__":
    rootPath = path.dirname(__file__)
    # TODO remove this nrows, caps number of ratings read to save memory
    ratings = pd.read_csv(path.join(rootPath, "data/ratings.csv"), nrows=10000)
    books = pd.read_csv(path.join(rootPath, "data/books.csv"))
    ratings_books = pd.merge(ratings, books, on="book_id")

    ratings_books = ratings_books.pivot_table(
        index="user_id", columns="title", values="rating").fillna(0)

    predicitionsDF = generatePredictionsDFBySingularValueDecomposition(
        ratings_books)

    app.run(port=8080, debug=True)
