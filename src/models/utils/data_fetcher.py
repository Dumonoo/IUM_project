import pandas as pd
from datetime import datetime


class DataFetcher:
    def __init__(self, track_columns) -> None:
        self.track_columns = (
            track_columns
            if track_columns != "all"
            else [
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
        )
        self.tracks = pd.read_json("data/tracks.jsonl", lines=True)
        self.tracks["year"] = self.tracks.apply(
            lambda x: self.get_track_year(x["release_date"]), axis=1
        )
        self.tracks = self.tracks.dropna(subset=["id", "name"])
        self.tracks.fillna(0, inplace=True)
        self.sessions = pd.read_json("data/sessions.jsonl", lines=True)
        self.users = pd.read_json("data/users.jsonl", lines=True)

    def get_songs(self, ids):
        return self.tracks[self.tracks["id"].isin(ids)][self.track_columns].values

    def get_by_index(self, i):
        return self.tracks.iloc[i]

    def get_validation_data(self):
        return [
            self._get_validation_data_for_user(user) for user in self.users["user_id"]
        ]

    def get_training_data(self):
        return self.tracks[self.track_columns].values

    def _get_validation_data_for_user(self, user):
        data = self.sessions
        data = data[data["user_id"] == user]
        data = data[data["event_type"] == "like"]
        data.sort_values("timestamp", inplace=True)
        data = data["track_id"].values
        return data

    def get_track_year(self, str_date):
        data_obj = None
        if len(str_date) == 4:
            data_obj = datetime.strptime(str_date, "%Y")
        elif len(str_date) == 7:
            data_obj = datetime.strptime(str_date, "%Y-%m")
        else:
            data_obj = datetime.strptime(str_date, "%Y-%m-%d")
        return data_obj.year

    def fetch_track_learnign_data(self, ids):
        tracks_vectors = []
        for id in ids:
            track_data = self.tracks[self.tracks["id"] == id]
            # Check if track exists in track_data
            track_vector = track_data[self.track_columns].values
            tracks_vectors.append(track_vector)
        return tracks_vectors


if __name__ == "__main__":
    print(DataFetcher().get_validation_data())
