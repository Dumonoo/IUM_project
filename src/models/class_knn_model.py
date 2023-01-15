import pandas as pd
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


from models.utils.data_fetcher import DataFetcher


class KNNClassifierModel:
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
        self.knn = KNeighborsClassifier(n_neighbors=10)
        self.model = NearestNeighbors(n_neighbors=10, algorithm="brute")

    def train(self, train):
        X = self.data_fethcher.get_training_for_songs(train)
        y = train["event_type"].values
        X = self.scaler.fit_transform(X)
        self.model.fit(X)
        self.knn.fit(X, y)

    def predict(self, data):
        all_tracks = self.data_fethcher.tracks
        formated = self.data_fethcher.get_training_for_songs(all_tracks)
        X = self.scaler.transform(formated)
        classes = self.knn.predict(X)
        all_tracks["prediction"] = classes
        return all_tracks[all_tracks["prediction"] != "skip"][["id", "prediction"]]

    def recommend(self, ids):
        predicted = self.predict()
        return predicted[predicted["prediction"] == "like"]["id"].values

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
