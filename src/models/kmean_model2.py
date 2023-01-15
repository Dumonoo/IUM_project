import numpy as np
from scipy.spatial.distance import cdist

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
import pandas as pd
from src.models.utils.data_loader import DataLoader
from matplotlib import pyplot as plt

choosen_cols = [
                # "popularity",  # 0.06
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

class KMeanModel:
    def __init__(self) -> None:
        self.data_obj = DataLoader()
        self.tracks_data = self.data_obj.get_tracks()
        self.scaler = StandardScaler()
        # n_clusters=20, 
        #                            verbose=False, n_jobs=4
        # , n_init=400
        self.model = KMeans(n_clusters=50, verbose=0, n_init='auto')
        self.training_data = self.tracks_data[choosen_cols]

    def train(self):
        X = self.training_data[choosen_cols].values
        X = self.scaler.fit_transform(X)
        self.scaled_data = X
        self.model.fit(X)
    
    def recommend2(self, user_id, session_id):
        # Najpopularniejsze gatunki w sesji session_id
        user_most_popular_genres_in_session = self.data_obj.get_user_popular_genres_in_session(user_id, session_id, 3)
        given_genre_tracks = self.data_obj.get_tracks_of_genres(user_most_popular_genres_in_session)
        # mozna usunac tracki ktore juz sluchal do tej pory

        # Ocena aktualnej sesji 
        user_session_info = self.data_obj.get_super_user_info(user_id, session_id)
        session_estaminate = user_session_info.groupby('track_id')['estimation'].sum().reset_index().sort_values(by='estimation',ascending=False)
        session_estaminate['popularity'] = self.data_obj.get_tracks_popularity(session_estaminate['track_id'].values)

        # Juz przesluchane utwory do tej pory
        listened_tracks = self.data_obj.get_listened_tracks(user_id, session_id)
        session_estaminate = session_estaminate.sort_values(['estimation', 'popularity'], ascending = [False, False])
        # session_estaminate = session_estaminate.loc[session_estaminate['estimation'] > 1]
        # print(session_estaminate)
        TOP_G = 3

        top_g_ids = session_estaminate['track_id'].values[:TOP_G]

        # Model 
        mean_vector = self._get_mean_vector(top_g_ids)
        # print(mean_vector)
        scaled_track_center = self.scaler.transform(mean_vector)
        scaled_track_center = self.scaler.transform(mean_vector.reshape(1, -1))
        distances = cdist(scaled_track_center, self.scaled_data, 'cosine')
        index = list(np.argsort(distances)[:, :13][0])
        rec_songs = self.tracks_data.iloc[index]
        rec_songs = rec_songs[['id', 'popularity']]
        
        # ranking_without_old = rec_songs[~rec_songs['id'].isin(listened_tracks)]
        rec_id = rec_songs.sort_values('popularity', ascending=False)['id'].values[:10]
        gen_id = list(given_genre_tracks.sample(10, weights='popularity')["id"].values)

        return rec_id
        gen_id = list(set(gen_id) - set(listened_tracks))[:5]
        return_ids = list(rec_id[:5]) + gen_id

        return return_ids
        # given_genre_tracks.sample(10, weights='popularity')["id"].values = self.data_obj.get_user_popular_genres_in_session(user_id, session_id, 3)
        # if(len(rec_id)<10):
        #     rec_id = list(rec_id) + list(self.tracks_data.sample(10-len(rec_id))['id'].values)
        #     return rec_id
        # # print(rec_id)
        # return rec_id

    def _get_mean_vector(self, top_id):
        song_vec = []
        for song in top_id:
            song_vec.append(self.tracks_data.loc[self.tracks_data['id'] ==  song][choosen_cols].values)
        return np.mean(np.array(list(song_vec)), axis=0)
    
    def test_elow(self):
        wcss = []
        for i in range(1, 50):
            kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init="auto", random_state=0)
            X = self.training_data[choosen_cols].values
            X = self.scaler.fit_transform(X)
            self.scaled_data = X
            # self.model.fit(X)
            kmeans.fit(self.scaled_data)
            wcss.append(kmeans.inertia_)
        plt.plot(range(1, 50), wcss)
        plt.title('Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.show()
