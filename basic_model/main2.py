import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from get_user_data import analyse_user
from data_fetcher import DataFetcher


class Model:
    def __init__(self) -> None:
        self.data_fetcher = DataFetcher()
        self.tracks = self.data_fetcher.tracks

    def train(self):
        clean_tracks = self._clean_tracks(self.tracks)
        self._fit_cluster(clean_tracks)

    def validate(self):
        self.train()
        all_rates = []
        for user in range(101, 151):
            rate = self.validate_for_user(user)
            if rate is None:
                continue
            all_rates.append(rate)
        print("Total rate:", sum(all_rates) / len(all_rates))

    def validate_for_user(self, user_id):
        n = 10
        userSessions = analyse_user(user_id)
        userSessions.sort_sessions_by_date()
        userSessions.all_session_list.reverse()
        liked, session_end = userSessions.get_n_first_liked(n)
        if not liked:
            return None
        recommended = self.recommend(liked)
        later_songs = userSessions.get_n_songs_listened_since(None, session_end)
        rating = len([song for song in recommended if song["id"] in later_songs]) / len(
            liked
        )
        return rating

    def recommend(self, liked, n=10):
        metadata_columns = ["id", "name", "year"]
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
        rec_songs = self.tracks.iloc[index]
        return rec_songs[metadata_columns].to_dict(orient="records")

    def _clean_tracks(self, df: pd.DataFrame):
        df = df.dropna(subset=["id"])
        return df

    def _fit_cluster(self, tracks: pd.DataFrame):
        self.pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("kmeans", KMeans(n_clusters=14, verbose=0, n_init="auto")),
            ],
        )
        X = self.data_fetcher.get_training_data()
        self.pipeline.fit(X)

    def _get_mean_vector(self, liked_ids):
        tracks_vectors = self.data_fetcher.fetch_track_learnign_data(liked_ids)
        tracks_matrix = np.array(list(tracks_vectors))
        return np.mean(tracks_matrix, axis=0)


if __name__ == "__main__":
    model = Model()
    # model.train()
    model.validate()
