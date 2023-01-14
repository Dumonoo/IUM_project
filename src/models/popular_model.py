from models.utils.data_fetcher import DataFetcher


class PopularModel:
    def __init__(self) -> None:
        self.fetcher = DataFetcher("id")
        ...

    def train(self):
        ...

    def recommend(self, ids):
        tracks = self.fetcher.tracks
        tracks = tracks[~tracks["id"].isin(ids)]
        test = tracks.sort_values(by=["popularity"]).tail(10)
        return test["id"].values
