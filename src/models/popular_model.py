from models.utils.data_fetcher import DataFetcher


class PopularModel:
    def __init__(self) -> None:
        self.fetcher = DataFetcher("id")
        ...

    def train(self, user):
        self.tracks = self.fetcher.get_training_data(user)

    def recommend(self, ids):
        self.tracks = self.tracks[~self.tracks["id"].isin(ids)]
        test = self.tracks.sort_values(by=["popularity"]).tail(10)
        return test["id"].values

    def reset(self):
        self.tracks = []
