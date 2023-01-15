from src.models.utils.data_loader import DataLoader

class RandomModelGenres:
    def __init__(self) -> None:
        self.data_obj = DataLoader()

    def train(self):
        ...

    def recommend2(self, user_id, session_id):
        # Na podstawie ostatnio 3 najczesceij sluchanych ostatnio kategorii losujemy z uwzglednieiem popularity
        user_most_popular_genres_in_session = self.data_obj.get_user_popular_genres_in_session(user_id, session_id, 3)
        given_genre_tracks = self.data_obj.get_tracks_of_genres(user_most_popular_genres_in_session)
        # mozna usunac tracki ktore juz sluchal do tej pory
        return given_genre_tracks.sample(10, weights='popularity')["id"].values


    def recommend(self, ids, usr_id):
        usr_fav_genres = self.data_obj.get_user_fav_genres(usr_id)
        genres_tracks = self.data_obj.get_tracks_of_genres(usr_fav_genres)
        # genres_tracks = self.data_obj.get_tracks()
        genres_tracks[~genres_tracks["id"].isin(ids)]
        # print(genres_tracks.sample(10))
        # return genres_tracks.sample(10, weights='popularity')["id"].values
        return genres_tracks.sample(10)["id"].values
        # return genres_tracks.sample(10, "popularity")["id"].values
