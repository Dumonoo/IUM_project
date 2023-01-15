from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import json
from models.utils.data_fetcher import DataFetcher


class CosineModel:
    def __init__(self) -> None:
        self.fetcher = DataFetcher(
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
        pass

    def train(self):
        songs = self.fetcher.tracks[self.fetcher.track_columns]
        X = self.scaler.fit_transform(songs)
        cosine_similarities = cosine_similarity(X)
        self.similarities = {
            self.fetcher.tracks.iloc[i]["id"]: self.fetcher.tracks.iloc[
                k.argsort()[:-50:-1]
            ]["id"].values.tolist()
            for i, k in enumerate(cosine_similarities)
        }

    def write(self):
        json.dump(self.similarities, open("cosine_similarities.json", "w"))

    def read(self):
        self.similarities = json.load(open("cosine_similarities.json"))

    def recommend_by_track(self, track):
        recommendations = self.similarities[track]
        return recommendations

    def limit_to_user(self, user):
        self.original_similaritites = self.similarities
        rated = self.fetcher.get_all_rated(user)["track_id"].values
        self.similarities = {
            k: [track for track in v if track in rated]
            for k, v in self.similarities.items()
            if k in rated
        }

    def unlimit(self):
        self.similarities = self.original_similaritites

    def recommend_to_user(self, user):
        liked = self.fetcher.get_all_liked_by_user(user)[:10]
        rated = self.fetcher.get_all_rated(user)["track_id"].values
        # print([track for track in liked if track not in self.fetcher.tracks["id"].values])
        return [
            recs[-1]
            for track in liked
            if (recs := self.recommend_by_track(track))
            and (recs := [t for t in recs if t not in liked])
        ]
        ...
