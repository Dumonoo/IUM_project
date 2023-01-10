from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from data_fetcher import DataFetcher
from get_user_data import analyse_user


class KNNModel:
    def __init__(self) -> None:
        self.data_fethcher = DataFetcher(
            [
                # "popularity", #0.06
                "duration_ms", #0.53
                # "explicit", #0.02
                # "danceability", #0.44
                # "energy", #0.48
                # "key", #0.02
                "loudness", #0.53
                # "speechiness", #0.48
                "acousticness", #0.51
                # "instrumentalness", #0.46
                "liveness", #0.53
                # "valence", #0.48
                "tempo", #0.53
                # "year", #0.04
                #
            ]
        )
        self.scaler = StandardScaler()
        self.model = NearestNeighbors(n_neighbors=10)

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
        n = 50
        userSessions = analyse_user(user_id)
        userSessions.sort_sessions_by_date()
        userSessions.all_session_list.reverse()
        liked, session_end = userSessions.get_n_first_liked(n)
        if not liked:
            return None
        recommended = self.recommend(liked)
        later_songs = userSessions.get_n_songs_listened_since(None, session_end)
        return 1 if any([song in later_songs for song in recommended]) else 0

    def train(self):
        X = self.data_fethcher.get_training_data()
        X = self.scaler.fit_transform(X)
        self.model.fit(X)

    def recommend(self, ids):
        songs = self.data_fethcher.get_songs(ids)
        X = self.scaler.transform(songs)
        _, indices = self.model.kneighbors(X)
        return self.data_fethcher.get_by_index(indices[0])["id"].values


if __name__ == "__main__":
    model = KNNModel()
    print(model.validate())
