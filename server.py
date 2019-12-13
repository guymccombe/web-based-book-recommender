from flask import Flask, render_template, make_response, abort, request, redirect, url_for, session, jsonify
from sys import argv

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
        user = session["username"]
        message, status = recommender.getRecommendations(user)
        return make_response(jsonify(message), status)
    else:
        abort(403)


@app.route("/rating", methods=["POST"])
def rate():
    if "username" not in session:
        return redirect(url_for("login"))
    else:
        title, rating = request.form.values()
        user = session["username"]
        message, status = recommender.addRating(user, title, float(rating))
        return make_response(message, status)


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def loginHandler():
    if "username" not in session:
        username = request.get_json()["username"]
        if (recommender.isUserInDB(username)):
            session["username"] = username
            return redirect(url_for("home"))
        else:
            message = "User not found, if you're new please register."
            return make_response(message, 404)
    else:
        abort(403)


@app.route("/register", methods=['POST'])
def registerHandler():
    if "username" not in session:
        username = request.get_json()["username"]
        if (recommender.isUserInDB(username)):
            message = "User already exists, try logging in if this is you."
            return make_response(message, 403)
        else:
            session["username"] = username
            return redirect(url_for("home"))
    else:
        abort(403)


@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username", None)
        recommender.backup()
    return redirect(url_for("login"))


@app.route("/delete")
def delete():
    if "username" in session:
        recommender.delete(session["username"])
        return redirect(url_for("logout"))
    else:
        abort(403)


if __name__ == "__main__":
    recommender = None
    if len(argv) > 0:
        try:
            cap = int(argv[1])
            recommender = Recommendations(cap)
        except:
            print(
                "Argument not recognised, please provide an int to cap the ratings to or nothing at all.")
            exit()
    else:
        recommender = Recommendations(None)

    app.run(port=8080, debug=True)
