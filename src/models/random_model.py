from models.utils.data_fetcher import DataFetcher
import random


fetcher = DataFetcher("id")


class RandomModel:
    def __init__(self, seed) -> None:
        self.seed = seed
        ...

    def train(self, user=None):
        self.data = fetcher.get_training_data(user)
        ...

    def recommend(self, ids):
        tracks = self.data
        tracks = tracks[~tracks["id"].isin(ids)]
        return tracks.sample(10, random_state=self.seed)["id"].values

    def reset(self):
        self.data = []
