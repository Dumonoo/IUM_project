from models.utils.data_fetcher import DataFetcher


class RandomModel:
    def __init__(self) -> None:
        self.fetcher = DataFetcher("id")
        ...

    def train(self):
        ...

    def recommend(self, ids):
        tracks = self.fetcher.tracks
        tracks = tracks[~tracks["id"].isin(ids)]
        return tracks.sample(10)["id"].values
