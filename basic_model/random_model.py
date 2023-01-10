from data_fetcher import DataFetcher


class RandomModel:
    def __init__(self) -> None:
        self.fetcher = DataFetcher("id")
        ...

    def train(self):
        ...

    def recommend(self, ids):
        return self.fetcher.tracks.sample(10)["id"].values
