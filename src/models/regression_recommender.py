import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from models.utils.data_fetcher import DataFetcher
import random


class RegressionRecommender:
    def __init__(self) -> None:
        # self.fetcher = DataFetcher()
        self.knn = KNeighborsRegressor(n_neighbors=1)
        self.scaler = StandardScaler()
        self.meta_columns = [
            "popularity",  # 0.06
            "duration_ms",  # 0.53
            "explicit",  # 0.02
            "danceability",  # 0.44
            "energy",  # 0.48
            "key",  # 0.02
            "loudness",  # 0.53
            "speechiness",  # 0.48
            "acousticness",  # 0.51
            "instrumentalness",  # 0.46
            "liveness",  # 0.53
            "valence",  # 0.48
            "tempo",  # 0.53
            "year",  # 0.04
            #
        ]

    def train(self, X, y):
        X = X[self.meta_columns].values
        X = self.scaler.fit_transform(X)
        self.knn.fit(X, y)

    def predict(self, songs):
        X = songs[self.meta_columns].values
        X = self.scaler.transform(X)
        return self.knn.predict(X)


class RandomRegression:
    def __init__(self) -> None:
        ...

    def train(self, X, y):
        ...

    def predict(self, songs):
        return songs.apply(lambda x: 1, axis=1)
        X = songs[self.meta_columns].values
        X = self.scaler.transform(X)
        return self.knn.predict(X)
