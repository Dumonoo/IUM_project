import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from datetime import datetime

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from get_user_data import analyse_user

used_columns = [
    "popularity",
    "duration_ms",
    "explicit",
    "danceability",
    "energy",
    "key",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "year",
]


class Model:
    def __init__(self, tracks: pd.DataFrame) -> None:
        self.tracks = tracks

    def train(self):
        self._fit_cluster(self.tracks)

    def validate(self):
        self.validate_for_user(101)

    def validate_for_user(self, user_id):
        userSessions = analyse_user(user_id)
        userSessions.sort_sessions_by_date()
        userSessions.all_session_list.reverse()
        for session in userSessions.all_session_list[:-1]:
            liked = session.get_songs_liked_set()
            later_songs = userSessions.get_songs_listened_since(
                session.session_end_timestamp
            )
            if not len(liked):
                continue
            self._fit_cluster(self.tracks)
            recommended = model.recommend(liked)
            print(*recommended, sep="\n")
            rate = len([song for song in recommended if song["id"] in later_songs])
            print("Rate:", rate)

    def _fit_cluster(self, tracks: pd.DataFrame):
        self.pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("kmeans", KMeans(n_clusters=14, verbose=0, n_init="auto")),
            ],
        )
        X = tracks.select_dtypes(np.number)
        X.fillna(0, inplace=True)
        self.pipeline.fit(X.values)

    def recommend(self, liked, n=10):
        metadata_columns = ["id", "name", "year"]
        mean_vector = self._get_mean_vector(liked)
        scaler = self.pipeline.steps[0][1]
        scaled_data = scaler.transform(self.tracks[used_columns].values)
        scaled_track_center = scaler.transform(mean_vector)
        scaled_track_center = scaler.transform(mean_vector.reshape(1, -1))
        distances = cdist(scaled_track_center, scaled_data, "cosine")
        index = list(np.argsort(distances)[:, :n][0])
        rec_songs = self.tracks.iloc[index]
        return rec_songs[metadata_columns].to_dict(orient="records")

    def _get_mean_vector(self, liked_ids):
        tracks_vectors = []
        for id in liked_ids:
            track_data = self._find_track_by_id(id)
            # Check if track exists in track_data
            track_vector = track_data[used_columns].values
            tracks_vectors.append(track_vector)

        tracks_matrix = np.array(list(tracks_vectors))
        return np.mean(tracks_matrix, axis=0)

    def _find_track_by_id(self, id):
        return self.tracks.loc[self.tracks["id"] == id]


def get_year(str_date):
    data_obj = None
    if len(str_date) == 4:
        data_obj = datetime.strptime(str_date, "%Y")
    elif len(str_date) == 7:
        data_obj = datetime.strptime(str_date, "%Y-%m")
    else:
        data_obj = datetime.strptime(str_date, "%Y-%m-%d")
    return data_obj.year


if __name__ == "__main__":

    tracks = pd.read_json("data/tracks.jsonl", lines=True)
    tracks["year"] = tracks.apply(lambda x: get_year(x["release_date"]), axis=1)
    model = Model(tracks)
    model.validate()
