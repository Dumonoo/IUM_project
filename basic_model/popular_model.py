from data_fetcher import DataFetcher


class PopularModel:
    def __init__(self) -> None:
        self.fetcher = DataFetcher("id")
        ...

    def train(self):
        ...

    def recommend(self, ids):
        self.tracks = self.fetcher.tracks
        test = self.tracks.sort_values(by=["popularity"]).tail(10)
        return test["id"].values
