from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

from models.utils.data_fetcher import DataFetcher


class KNNModel:
    def __init__(self) -> None:
        self.data_fethcher = DataFetcher(
            [
                # "popularity", #0.06
                "duration_ms",  # 0.53
                # "explicit", #0.02
                # "danceability", #0.44
                # "energy", #0.48
                # "key", #0.02
                "loudness",  # 0.53
                # "speechiness", #0.48
                "acousticness",  # 0.51
                # "instrumentalness", #0.46
                "liveness",  # 0.53
                # "valence", #0.48
                "tempo",  # 0.53
                # "year", #0.04
                #
            ]
        )
        self.scaler = StandardScaler()
        self.model = NearestNeighbors(n_neighbors=10)

    def train(self):
        X = self.data_fethcher.get_training_data()
        X = self.scaler.fit_transform(X)
        self.model.fit(X)

    def recommend(self, ids):
        songs = self.data_fethcher.get_songs(ids)
        X = self.scaler.transform(songs)
        _, indices = self.model.kneighbors(X)
        return self.data_fethcher.get_by_index(indices[0])["id"].values
