from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd
from models.utils.data_loader import DataLoader

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
            n_neighbors=5, metric="cosine"
            , algorithm="auto"
        )
        self.training_data = self.tracks_data[choosen_cols]

    def train(self):
        X = self.training_data[choosen_cols].values
        X = self.scaler.fit_transform(X)
        self.model.fit(X)

    def recommend(self, user_id, session_id):
        # Najpopularniejsze gatunki w sesji session_id
        user_most_popular_genres_in_session = self.data_obj.get_user_popular_genres_in_session(user_id, session_id, 3)
        given_genre_tracks = self.data_obj.get_tracks_of_genres(user_most_popular_genres_in_session)
        usr_fav_genres = self.data_obj.get_user_fav_genres(user_id)
        genres_tracks = self.data_obj.get_tracks_of_genres(usr_fav_genres)
                # Ocena aktualnej sesji 
        user_session_info = self.data_obj.get_super_user_info(user_id, session_id)
        session_estaminate = user_session_info.groupby('track_id')['estimation'].sum().reset_index().sort_values(by='estimation',ascending=False)
        session_estaminate['popularity'] = self.data_obj.get_tracks_popularity(session_estaminate['track_id'].values)
        session_estaminate = session_estaminate.sort_values(['estimation', 'popularity'], ascending = [False, False])
        TOP_G = 3

        top_g_ids = session_estaminate['track_id'].values[:TOP_G]

        input_songs_data = self.tracks_data[self.tracks_data['id'].isin(top_g_ids)][choosen_cols].values

        # Model
        X = self.scaler.transform(input_songs_data)
        distances, indices = self.model.kneighbors(X)
        recommended_indexes = [x for line in indices for x in line]
        recommended_id = self.data_obj.get_ids_of_given_ids(recommended_indexes)

        ranking = pd.DataFrame({'id': recommended_id, 'popularity': self.data_obj.get_tracks_popularity(recommended_id)})

        rec_id = list(ranking.sort_values('popularity', ascending=False)['id'].values[:10])
        gen_id = list(given_genre_tracks.sample(15, weights='popularity')["id"].values)
        fgen_id = list(genres_tracks.sort_values('popularity', ascending=False)['id'].values[:10])

        return_tab = []
        while len(return_tab) != 10:
            if len(return_tab) != 10:
                if gen_id[0] not in return_tab:
                    return_tab.append(gen_id.pop(0))
                else:
                    gen_id.pop(0)

            if len(return_tab) != 10:
                if rec_id[0] not in return_tab:
                    return_tab.append(rec_id.pop(0))
                else:
                    rec_id.pop(0)

            if len(return_tab) != 10: 
                if fgen_id[0] not in return_tab:
                    return_tab.append(fgen_id.pop(0))
                else:
                    fgen_id.pop(0)

        return return_tab

