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
        self.users = pd.read_json("data/users.jsonl", lines=True)
        self.read_tracks()
        self.read_sessions()

    def read_tracks(self):
        df = pd.read_json("data/tracks.jsonl", lines=True)
        df["year"] = df.apply(lambda x: self.get_track_year(x["release_date"]), axis=1)
        df = df.dropna()
        self.tracks = df

    def read_sessions(self):
        self.sessions = (
            pd.read_json("data/sessions.jsonl", lines=True)
            .dropna(subset=["user_id", "track_id", "event_type"])
            .sort_values(by="timestamp")
            # .drop_duplicates(subset=["user_id", "track_id"], keep="last")
        )
        self.sessions = self.sessions[
            self.sessions["track_id"].isin(self.tracks["id"].values)
        ]

    def read_avg_listen(self, user):
        user_sessions = self.sessions[self.sessions["user_id"] == user]
        user_tracks = self.tracks[
            self.tracks["id"].isin(user_sessions["track_id"].values)
        ]
        listened = user_tracks.apply(
            lambda x: self.count_avg_for_track(x, user_sessions), axis=1
        )
        user_tracks = user_tracks.assign(listened=listened)
        user_tracks = user_tracks.assign(label=listened.apply(lambda x: x > 0.75))
        max_size = user_tracks["label"].value_counts().max()
        lst = [user_tracks]
        for class_index, group in user_tracks.groupby("label"):
            n = max_size - len(group)
            lst.append(group.sample(n // 2, replace=True))
        df = pd.concat(lst)
        return df, df["listened"]

    def count_avg_for_track(self, track, sessions):
        listened = []
        df = sessions[sessions["track_id"] == track["id"]]
        if len(df[df["event_type"] == "like"]):
            return 1
        prev_play_time = None
        for i, row in df.iterrows():
            if row["event_type"] == "play":
                listened.append(1)
                prev_play_time = row["timestamp"]
            elif row["event_type"] == "skip":
                if prev_play_time is None:
                    continue
                listened.pop()
                listened.append(
                    ((row["timestamp"] - prev_play_time).seconds)
                    / (track["duration_ms"] / 1000)
                )
        return sum(listened) / len(listened) if len(listened) else 0

        return 0

    def get_all_rated(self, user):
        return self.sessions[self.sessions["user_id"] == user]
        ...

    def get_all_liked_by_user(self, user):
        user_sessions = self.sessions[self.sessions["user_id"] == user]
        return user_sessions[user_sessions["event_type"] == "like"]["track_id"].values

    def get_all_skipped_by_user(self, user):
        user_sessions = self.sessions[self.sessions["user_id"] == user]
        return user_sessions[user_sessions["event_type"] == "skip"]["track_id"].values

    def get_all_listened_to_by_user(self, user):
        user_sessions = self.sessions[self.sessions["user_id"] == user]
        return user_sessions[user_sessions["event_type"] == "play"]["track_id"].values

    def get_songs(self, ids):
        return self.tracks[self.tracks["id"].isin(ids)][self.track_columns].values

    def get_by_index(self, i):
        return self.tracks.iloc[i]

    def get_validation_data(self):
        return [
            self._get_validation_data_for_user(user) for user in self.users["user_id"]
        ]

    def get_training_for_songs(self, songs):
        return self.tracks[self.tracks["id"].isin(songs["id"].values)][
            self.track_columns
        ].values

    def get_columns(self, songs):

        return self.tracks[self.tracks["id"].isin(songs)][self.track_columns].values

    def get_training_data(self, user):
        if user is None:
            return self.tracks
        else:
            liked = self.get_all_liked_by_user(user)
            listened = self.get_all_listened_to_by_user(user)
            skipped = self.get_all_skipped_by_user(user)
            sessions = self.get_all_rated(user)
            rated_tracks = sessions["track_id"].values
            return self.tracks[self.tracks["id"].isin(rated_tracks)]

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

    def get_user_item_matrix(self):
        sessions = self.sessions
        sessions["rating"] = self.sessions.apply(
            lambda x: {"like": 2, "play": 1, "skip": -1}[x["event_type"]],
            axis=1,
        )
        ratings = sessions.pivot(index="track_id", columns="user_id", values="rating")
        ratings = ratings.fillna(0)
        return ratings


if __name__ == "__main__":
    print(DataFetcher().get_validation_data())
