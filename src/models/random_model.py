from models.utils.data_fetcher import DataFetcher


class RandomModel:
    def __init__(self) -> None:
        self.fetcher = DataFetcher("id")
        ...

    def train(self, user=None):
        self.data = self.fetcher.get_training_data(user)
        ...

    def recommend(self, ids):
        tracks = self.data
        tracks = tracks[~tracks["id"].isin(ids)]
        return tracks.sample(10)["id"].values

    def reset(self):
        self.data = []
