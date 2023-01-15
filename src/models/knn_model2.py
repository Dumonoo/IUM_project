from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

from src.models.utils.data_loader import DataLoader

from collections import Counter

choosen_cols = [
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
                # "year",  # 0.04
                #
            ]

class KNNModel:
    def __init__(self) -> None:
        self.data_obj = DataLoader()

        self.tracks_data = self.data_obj.get_tracks()
        self.scaler = StandardScaler()
        self.model = NearestNeighbors(
            n_neighbors=5, metric="cosine", algorithm="brute"
        )
        self.training_data = self.tracks_data[choosen_cols]

    def train(self):
        X = self.training_data[choosen_cols].values
        X = self.scaler.fit_transform(X)
        self.model.fit(X)

    def recommend2(self, user_id, session_id):
        # Na podstawie 
        ...


    def recommend(self, ids, user_id):
        # print(ids)
        input_songs_data = self.tracks_data[self.tracks_data['id'].isin(ids)][choosen_cols].values
        input_indexes = self.data_obj.get_indexes_of_tracks(ids)
        X = self.scaler.transform(input_songs_data)
        distances, indices = self.model.kneighbors(X)
        score_board = {}
        counter2 = Counter()
        for d, i in zip(distances, indices):
            for x in range(len(d)):
                if i[x]  in input_indexes:
                    continue
                if i[x] not in score_board:
                    score_board[i[x]] = d[x]
                else:
                    score_board[i[x]] = min(d[x], score_board[i[x]])
        recomended_index = [key for key, value in sorted(score_board.items(), key=lambda item: item[1])]
        recommended_id = self.data_obj.get_ids_of_given_ids(recomended_index[:10])
        counter = Counter()
        for track in recommended_id:
            counter[self.data_obj.get_track_popularity(track)] += 1
            counter2[self.data_obj.get_track_popularity(track)] += 1
        # recommended_id = self.data_obj.get_ids_of_given_ids(recomended_index)
        print("halo", counter2)

        usr_fav_genres = self.data_obj.get_user_fav_genres(user_id)
        genres_tracks = self.data_obj.get_tracks_of_genres(usr_fav_genres)

        # Podaj max 8 utworow z ulubionych generes
        genres_rec_ids = []
        not_ids = []
        for i in recommended_id:
            if not genres_tracks.loc[genres_tracks['id'] == i].empty:
                genres_rec_ids.append(i)
            else:
                not_ids.append(i)
        
        # recommended_id = genres_rec_ids + not_ids

        # print("TTT", genres_tracks)

        return recommended_id[:10]