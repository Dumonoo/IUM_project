#!/usr/bin/env python3


import pandas as pd

users = pd.read_json("data/users.jsonl", lines=True)
sessions = pd.read_json("data/sessions.jsonl", lines=True)

# Returns all user sessions cleaned from advertisments
def get_user_sessions_info(user_id):
    sessions_info = sessions.loc[sessions["user_id"] == user_id]
    sessions_info = sessions_info.loc[sessions_info['event_type'] != "advertisment"]
    return sessions_info

def get_user_sessions_list(user_id):
    sessions_info = get_user_sessions_info(user_id=user_id)
    return sessions_info.groupby(by=['session_id'], group_keys=True).apply(lambda x: x)

# Procedure Analyse sessions for user -> limit session data -> use prediction to guess user playlist -> check if its in future user session
# Normaly -> get lates users sessions analyse best more liked tracks -> send it to model to calculate best tracks for listen 
# -> exclude any skiped tracks from list, exclude any track which was listend in previous month
# Return to user list of 10 best tracks for him dont forget to add one / two random track from time to time to exploration
class Session:
    def __init__(self, session_id):
        self.id = session_id
        self.session_start_timestamp = None
        self.session_end_timestamp = None
        self.session_songs_listened_ids = []
        self.session_songs_skiped_ids = []
        self.session_song_liked_ids = []
        self.session_data = []
        self.session_length = 0

    # User lisened to this song
    def add_song(self, id):
        self.session_songs_listened_ids.append(id)

    # User didnt like this song much
    def add_skipped_song(self, id):
        self.session_songs_skiped_ids.append(id)

    # User liked this song
    def add_liked_song(self, id):
        self.session_song_liked_ids.append(id)

    # Update session timestamps and session length
    def update_timestamps(self, start_time, end_time):
        self.session_start_timestamp = start_time
        self.session_end_timestamp = end_time
        self.session_length = end_time = start_time

    # Add pandas row to session data array
    def add_session_data(self, row):
        self.session_data.append(row)

    # Return list of tracks id which were litended during session
    def get_songs_listened_set(self):
        return list(set(self.session_songs_listened_ids))

    # Return list of tracks id which were skipped during session
    def get_songs_skipped_set(self):
        return list(set(self.session_songs_skiped_ids))

    # Return list of tracks id which were liked during session
    def get_songs_liked_set(self):
        return list(set(self.session_song_liked_ids))

    # Return list of tracks id listend during session exclude skipped
    def get_song_listened_without_skiping(self):
        filtered_tracks = []
        skipped_tracks = self.get_songs_skipped_set()
        for track in self.get_songs_listened_set():
            if track not in skipped_tracks:
                filtered_tracks.append(track)
        return filtered_tracks



    pass
class UserSessions:
    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.session_list = []
        self.furute_session_list = []
        # All sessions before clamping
        self.all_session_list = []
        self.sorted = False
    
    # Sort session by date ascending
    def sort_sessions_by_date(self):
        if self.sorted:
            return
        self.session_list = sorted(self.session_list, key=lambda session: session.session_end_timestamp, reverse=True)
        self.all_session_list = self.session_list
        self.sorted = True

    # Add session to the session list
    def add_session(self, session):
        self.session_list.append(session)

    # Get latest session
    def get_latest_session(self):
        self.sort_sessions_by_date()
        return self.session_list[0]

    # Get latest session to specific date
    def get_latest_session_to_date(self, timestamp):
        # set session_list to all before timestamp
        # set furute_session_list to all after timestamp
        pass
    
    # Get list of all tracks listened in previous x days
    def get_list_of_tracks_listened_in_previous_x_days(self, x_days = 30):
        last_day = self.get_latest_session().session_start_timestamp
        crit_day = last_day - pd.Timedelta(days=x_days)
        x_days_history = []
        for session in self.session_list:
            if session.session_end_timestamp < crit_day:
                break
            x_days_history.extend(session.get_songs_listened_set())
        return list(set(x_days_history))

    # Get list of all tracks listened in previous x days without skipped
    def get_list_of_tracks_listened_in_previous_x_days_without_skipping(self, x_days = 30):
        last_day = self.get_latest_session().session_start_timestamp
        crit_day = last_day - pd.Timedelta(days=x_days)
        x_days_history = []
        for session in self.session_list:
            if session.session_end_timestamp < crit_day:
                break
            x_days_history.extend(session.get_song_listened_without_skiping())
        return list(set(x_days_history))

    # Get list of all tracks skiped in previous x days
    def get_list_of_tracks_skiped_in_previous_x_days(self, x_days = 30):
        last_day = self.get_latest_session().session_start_timestamp
        crit_day = last_day - pd.Timedelta(days=x_days)
        x_days_history = []
        for session in self.session_list:
            if session.session_end_timestamp < crit_day:
                break
            x_days_history.extend(session.get_songs_skipped_set())
        return list(set(x_days_history))

    # Get list of all tracks liked in previous x days
    def get_list_of_tracks_liked_in_previous_x_days(self, x_days = 30):
        last_day = self.get_latest_session().session_start_timestamp
        crit_day = last_day - pd.Timedelta(days=x_days)
        x_days_history = []
        for session in self.session_list:
            if session.session_end_timestamp < crit_day:
                break
            x_days_history.extend(session.get_songs_liked_set())
        return list(set(x_days_history))



def analyse_user(user_id):
    user_session_obj = UserSessions(user_id)
    sessions = get_user_sessions_info(user_id)

    # Session information clamp
    current_session_id = None
    current_session_start = None
    current_session_end = None
    session_obj = None
    for index, row in sessions.iterrows():
        # First analyze session
        if current_session_id is None:
            current_session_id = row['session_id']
            session_obj = Session(current_session_id)

        # Next session
        if current_session_id != row['session_id']:
            session_obj.update_timestamps(current_session_start, current_session_end)
            user_session_obj.add_session(session_obj)
            current_session_id = row['session_id']
            current_session_start = None
            current_session_end = None
            session_obj = Session(current_session_id)
        
        # Start Time
        if current_session_start is None or current_session_start > row['timestamp']:
            current_session_start = row['timestamp']
        # End Time
        if current_session_end is None or current_session_end <= row['timestamp']:
            current_session_end = row['timestamp']

        # Songs played
        if row['event_type'] == "play":
            session_obj.add_song(row['track_id'])
        if row['event_type'] == "like":
            session_obj.add_liked_song(row['track_id'])
        if row['event_type'] == "skip":
            session_obj.add_skipped_song(row['track_id'])

    return user_session_obj

print("Hello world")
# print(analyse_user(101).get_latest_session().get_songs_listened_set())
# print(analyse_user(101).get_list_of_tracks_skiped_in_previous_x_days())
print(analyse_user(101).get_list_of_tracks_liked_in_previous_x_days())
