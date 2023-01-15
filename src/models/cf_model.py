from models.utils.data_fetcher import DataFetcher
from sklearn.neighbors import NearestNeighbors

import json


class CFModel:
    def __init__(self) -> None:
        self.fetcher = DataFetcher("all")
        self.knn = NearestNeighbors(n_neighbors=10, metric="cosine", algorithm="brute")

    def train(self):
        self.matrix = self.fetcher.get_user_item_matrix()
        self.knn.fit(self.matrix)

    def recommened(self, user):
        tracks = self.fetcher.get_all_liked_by_user(user)
        user_pref = self.matrix[self.matrix.index.isin(tracks)]
        dist, neighbors = self.knn.kneighbors(user_pref)
        neighbors = set([n for row in neighbors for n in row])
        neighbors = self.fetcher.get_by_index(list(neighbors))["id"].values
        return neighbors
        ...

    def reset():
        ...
