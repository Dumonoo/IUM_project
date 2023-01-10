import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from get_user_data import analyse_user
from data_fetcher import DataFetcher


class KMeanModel:
    def __init__(self) -> None:
        self.data_fetcher = DataFetcher(
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
            ]
        )
        self.tracks = self.data_fetcher.tracks

    def train(self):
        self.pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("kmeans", KMeans(n_clusters=14, verbose=0, n_init="auto")),
            ],
        )
        X = self.data_fetcher.get_training_data()
        self.pipeline.fit(X)

    def recommend(self, liked, n=10):
        # metadata_columns = ["id", "name", "year"]
        metadata_columns = ["id"]
        liked = [track for track in liked if track in self.tracks["id"].unique()]
        if not liked:
            return []
        mean_vector = self._get_mean_vector(liked)
        scaler = self.pipeline.steps[0][1]
        scaled_data = scaler.transform(self.data_fetcher.get_training_data())
        scaled_track_center = scaler.transform(mean_vector)
        scaled_track_center = scaler.transform(mean_vector.reshape(1, -1))
        distances = cdist(scaled_track_center, scaled_data, "cosine")
        index = list(np.argsort(distances)[:, :n][0])
        # print(index)
        rec_songs = self.tracks.iloc[index]
        return rec_songs[metadata_columns].values

    def _get_mean_vector(self, liked_ids):
        tracks_vectors = self.data_fetcher.fetch_track_learnign_data(liked_ids)
        tracks_matrix = np.array(list(tracks_vectors))
        return np.mean(tracks_matrix, axis=0)
