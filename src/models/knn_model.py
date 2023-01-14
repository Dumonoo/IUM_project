from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

from models.utils.data_fetcher import DataFetcher


class KNNModel:
    def __init__(self) -> None:
        self.data_fethcher = DataFetcher(
            [
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
        )
        self.scaler = StandardScaler()
        self.model = NearestNeighbors(
            n_neighbors=10, metric="cosine", algorithm="brute"
        )

    def train(self, user=None):
        self.data = self.data_fethcher.get_training_data(user)
        X = self.data_fethcher.get_training_for_songs(self.data)
        X = self.scaler.fit_transform(X)
        self.model.fit(X)

    def recommend(self, ids):
        songs = self.data_fethcher.get_songs(ids)
        X = self.scaler.transform(songs)
        distances, indices = self.model.kneighbors(X)
        indices = [self.data.iloc[row]["id"].values for row in indices]
        indices = [index for row in indices for index in row]
        distances = [dist for row in distances for dist in row]
        recommended = zip(indices, distances)

        recommended = [v for v in recommended if v[0] not in ids]
        recommended = sorted(recommended, key=lambda x: x[1])[-10:]
        recommended = [index for index, dist in recommended]
        return recommended

    def reset(self):
        self.scaler = StandardScaler()
        self.model = NearestNeighbors(
            n_neighbors=10, metric="cosine", algorithm="brute"
        )
