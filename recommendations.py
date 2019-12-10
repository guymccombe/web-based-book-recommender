'''
Recommendations class by singular value decomposition.
Based on a tutorial by Nick Becker:
https://beckernick.github.io/matrix-factorization-recommender/
'''

from os import path
from scipy.sparse.linalg import svds
import pandas as pd
import numpy as np


class Recommendations:
    books = pd.DataFrame()
    ratings = pd.DataFrame()
    ratings_books = pd.DataFrame()
    predictionsDF = pd.DataFrame()

    def __init__(self):
        rootPath = path.dirname(__file__)
        self.ratings = pd.read_csv(  # nrows to reduce memory usage during development
            path.join(rootPath, "data/ratings.csv"), nrows=100000)
        self.books = pd.read_csv(path.join(rootPath, "data/books.csv"))

        self.ratings_books = self.ratings.pivot_table(
            index="user_id", columns="book_id", values="rating").fillna(0)

        self.generatePredictionsDFBySingularValueDecomposition()

    def generatePredictionsDFBySingularValueDecomposition(self):
        values = self.ratings_books.values
        user_ratings_mean = np.mean(values, axis=1).reshape(-1, 1)
        demeaned = values - user_ratings_mean
        del values

        userFeaturesMatrix, weights, bookFeaturesMatrix = svds(
            demeaned, k=50)
        del demeaned
        weights = np.diag(weights)

        userPredictionRatings = np.dot(
            np.dot(userFeaturesMatrix, weights), bookFeaturesMatrix) + user_ratings_mean
        predicitions = pd.DataFrame(
            userPredictionRatings, columns=self.ratings_books.columns)

        self.predicitionsDF = predicitions

    def getRecommendations(self, userID, numberOfRecommendations=100):
        sortPred = self.predicitionsDF.iloc[userID].sort_values(
            ascending=False)

        userData = self.ratings[self.ratings.user_id == userID]
        userFull = (userData.merge(self.books, how="left", left_on="book_id",
                                   right_on="book_id").
                    sort_values(['rating'], ascending=False))

        print(f"User {userID} has already rated {userFull.shape[0]} books.")
        print(f"Recommending the highest {numberOfRecommendations} ratings.")

        recommendations = (
            self.books[~self.books["book_id"].isin(userFull["book_id"])].
            merge(pd.DataFrame(sortPred).reset_index(),
                  how="left", left_on="book_id",
                  right_on="book_id").
            rename(columns={userID: "Predictions"}).
            sort_values("Predictions", ascending=False).
            iloc[:numberOfRecommendations, :-1]["book_id"]
        )
        return [self.getTitleFromID(x) for x in recommendations]

    def getTitleFromID(self, ID):
        return self.books.loc[self.books["book_id"] == ID, "title"].values[0]

    def getIDFromTitle(self, title):
        return self.books.loc[self.books["title"] == title, "book_id"].values[0]

    def isUserInDB(self, username):
        return self.ratings["user_id"].isin([username]).any()
