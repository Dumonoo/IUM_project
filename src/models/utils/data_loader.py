import pandas as pd
from datetime import datetime
from typing import List

class DataLoader:
    def __init__(self):
        self.users = pd.read_json("data/users.jsonl", lines=True)
        self.artists = pd.read_json("data/artists.jsonl", lines=True)
        self.sessions = pd.read_json("data/sessions.jsonl", lines=True)
        self.tracks = pd.read_json("data/tracks.jsonl", lines=True)

        # Transformations
        self.users_transoformations()
        self.artists_transoformations()
        self.sessions_transoformations()
        self.tracks_transoformations()

    # Grabbers ???
    def get_tracks_of_genres(self, genres: List[str])-> List[str]:
        tracks_of_genres = []
        if genres:
            all_tracks_with_artist_genres = self.get_tracks()[['id', 'id_artist', 'name']].join(self.get_artists()[['id', 'genres']].set_index('id'), on='id_artist')
            tracks_of_genres = all_tracks_with_artist_genres[all_tracks_with_artist_genres['genres'].apply(lambda x: any(i in x for i in genres))]
            tracks_of_genres =  tracks_of_genres[['id', 'name', 'genres']]

        return tracks_of_genres


    def get_user_fav_genres(self, user_id: int)-> List[str]:
        return self.get_users().loc[self.get_users()["user_id"] == user_id]['favourite_genres'].values[0]


    def get_user_sessions(self, user_id: int):
        return self.sessions[self.sessions["user_id"] == user_id]

    def get_user_sessions_with_estimations(self, user_id: int):
        estimations = self.get_user_sessions(user_id)
        estimations['estimation'] = estimations.apply(lambda x: 1 if x['event_type'] == 'play' or x['event_type'] == 'like'  else 0, axis=1)
        prev_row = None
        for index, row in estimations.iterrows():
            ...
            if prev_row is None:
                prev_row = row
            else:
                if row['estimation'] == 0:
                    time_start = prev_row['timestamp']
                    time_end = row['timestamp']
                    time_diff_ms = int((time_end - time_start).total_seconds() * 1000)
                    # narazie linowo -> powinna by logarytmicza przy podstawie 1/2 i podniesiona troche
                    estimations.loc[index, 'estimation'] = -1 * (1 - (time_diff_ms / self.get_track_length_ms(row['track_id'])))
                if row['event_type'] != 'like':
                    prev_row = row

        return estimations
    
    def get_sessions_list_in_order(self, user_id: int):
        return list(self.get_user_sessions(user_id)['session_id'].unique())

    def get_user_history_without_sessions(self, user_id: int, session_ids: List[int]):
        ...

    def get_input_and_check_ids(self, user_id: int, history_ids:List[int], future_ids:List[int]):
        input_ids = None
        check_ids = None
        for h in history_ids:
            if input_ids is None:
                input_ids = self.combined_session_info(user_id, h)
            else:
                input_ids = pd.concat([input_ids, self.combined_session_info(user_id, h)])
        input_ids = input_ids.groupby('track_id')['estimation'].sum().reset_index().sort_values(by='estimation',ascending=False)

        for f in future_ids:
            if check_ids is None:
                check_ids = self.combined_session_info(user_id, f)
            else:  
                check_ids = pd.concat([input_ids, self.combined_session_info(user_id, f)])
        check_ids = check_ids.groupby('track_id')['estimation'].sum().reset_index().sort_values(by='estimation',ascending=False)      
        return input_ids, check_ids

    def get_input_and_check_ids_new(self, user_id: int, history_ids:List[int], future_ids:List[int], estaminators):
        input_ids = None
        check_ids = None
        for h in history_ids:
            if input_ids is None:
                input_ids = self.combined_session_info_new(user_id, h, estaminators)
            else:
                input_ids = pd.concat([input_ids, self.combined_session_info_new(user_id, h, estaminators)])
        input_ids = input_ids.groupby('track_id')['estimation'].sum().reset_index().sort_values(by='estimation',ascending=False)

        for f in future_ids:
            if check_ids is None:
                check_ids = self.combined_session_info_new(user_id, f, estaminators)
            else:  
                check_ids = pd.concat([check_ids, self.combined_session_info_new(user_id, f, estaminators)])
        check_ids = check_ids.groupby('track_id')['estimation'].sum().reset_index().sort_values(by='estimation',ascending=False)    
        return input_ids, check_ids

    def calcate_score(self, recommended_ids:List[str], check_ids):
        # print(recommended_ids, check_ids)
        score = 0
        for index, row in check_ids[check_ids['track_id'].isin(recommended_ids)].iterrows():
            score += row['estimation']
        # print("Score: ", score)
        return score/len(recommended_ids)


    # zwraca track_id i ocene utworu dla danej sesji
    def combined_session_info(self, user_id: int, session_id: int):
        assesments = self.get_user_sessions_with_estimations(user_id)
        assesments = assesments.loc[assesments['session_id'] == session_id]
        return assesments.groupby('track_id')['estimation'].sum().reset_index().sort_values(by='estimation',ascending=False)

    def combined_session_info_new(self, user_id: int, session_id: int, assessment_data):
        assesments = assessment_data
        assesments = assesments.loc[assesments['session_id'] == session_id]
        return assesments.groupby('track_id')['estimation'].sum().reset_index().sort_values(by='estimation',ascending=False)

    def get_track_listen_count_by_user(self, user_id: int, track_id: str):
        usr_session = self.get_user_sessions(user_id)
        return usr_session['track_id'].value_counts().get("track_id", 0)

    
    def get_track_length_ms(self, track_id: str):
        return self.get_tracks().loc[self.get_tracks()['id'] == track_id]['duration_ms'].values[0]
        ...

    # Data transformations
    def users_transoformations(self):
        self.users = self.users[["user_id", "favourite_genres"]]
    
    def artists_transoformations(self):
        ...
    
    def sessions_transoformations(self):
        self.sessions = self.sessions.loc[self.sessions["event_type"] != "advertisment"]
        self.sessions = self.sessions.sort_values(by="timestamp")
        self.sessions['date'] = self.sessions.apply(lambda x: x['timestamp'].date(), axis=1)
    

    def tracks_transoformations(self):
        self.tracks["year"] = self.tracks.apply(
            lambda x: self.get_track_year(x["release_date"]), axis=1
        )
        self.tracks = self.tracks.dropna(subset=["id", "name"])
        self.tracks.fillna(0, inplace=True)

    # Additional Functions
    def get_track_year(self, str_date):
        data_obj = None
        if len(str_date) == 4:
            data_obj = datetime.strptime(str_date, "%Y")
        elif len(str_date) == 7:
            data_obj = datetime.strptime(str_date, "%Y-%m")
        else:
            data_obj = datetime.strptime(str_date, "%Y-%m-%d")
        return data_obj.year

    def get_estimation(self, listened_ms: int, duration_ms: int):
        return 0
        
    # Getters - irrelevant
    def get_users(self):
        return self.users
    
    def get_artists(self):
        return self.artists
    
    def get_sessions(self):
        return self.sessions

    def get_tracks(self):
        return self.tracks

    def get_tracks_for_model(self, columns):
        track_columns = (
            columns
            if columns != "all"
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
        return self.get_tracks()[track_columns]

    def get_indexes_of_tracks(self, track_list_ids: List[str]):
        ids_list = []
        for track_id in track_list_ids:
            ids_list.append(self.tracks.loc[self.tracks['id'] == track_id].index[0])
        return ids_list

    def get_ids_of_given_ids(self, track_indexes):
        return self.tracks.iloc[track_indexes]['id'].values

    # Analysis purposes
    def get_life(self, user_id:int):
        user_sessions = self.get_sessions_list_in_order(user_id)

        return user_sessions
        ...
