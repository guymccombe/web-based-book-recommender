from flask import Flask, Response, render_template, request, abort, redirect, url_for, session, jsonify
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
def recommend():
    if "username" in session:
        return jsonify(getRecommendations(session["username"]))
    else:
        abort(403)


def getRecommendations(username, numberOfRecommendations=100):
    userID = userNameToID(username)
    sortPred = predicitionsDF.iloc[userID].sort_values(ascending=False)

    userData = ratings[ratings.user_id == userID]
    userFull = (userData.merge(books, how="left", left_on="book_id",
                               right_on="book_id").
                sort_values(['rating'], ascending=False))

    print(f"User {userID} has already rated {userFull.shape[0]} books.")
    print(f"Recommending the highest {numberOfRecommendations} ratings.")

    recommendations = (
        books[~books["book_id"].isin(userFull["book_id"])].
        merge(pd.DataFrame(sortPred).reset_index(),
              how="left", left_on="title",
              right_on="title").
        rename(columns={userID: "Predictions"}).
        sort_values("Predictions", ascending=False).
        iloc[:numberOfRecommendations, :-1]["title"]
    )
    return recommendations.tolist()


def userNameToID(username):
    # TODO permanent solution instead of casting username to int
    return int(username)


@app.route("/rating", methods=["POST"])
def rate():
    if "username" not in session:
        return redirect(url_for("login"))
    else:
        newRating = request.form.values()
        addRating(*newRating)
        return redirect(url_for("home"))


def addRating(title, rating, genre):
    print(ratings_books.tail())
    ratings_books.loc[str(
        992), "'Salem's Lot The Illustrated Edition"] = float(rating)
    print(ratings_books.tail())
    generatePredictionsDFBySingularValueDecomposition(ratings_books)


@app.route("/login", methods=["GET"])
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
    ratings = pd.read_csv(  # nrows to reduce memory usage during development
        path.join(rootPath, "data/ratings.csv"), nrows=100000)
    books = pd.read_csv(path.join(rootPath, "data/books.csv"))
    ratings_books = pd.merge(ratings, books, on="book_id")

    ratings_books = ratings_books.pivot_table(
        index="user_id", columns="title", values="rating").fillna(0)

    predicitionsDF = generatePredictionsDFBySingularValueDecomposition(
        ratings_books)

    app.run(port=8080, debug=True)
