#!/usr/bin/env python3

from os import listdir
from os.path import isfile

import pandas as pd
from IPython.display import display
from IPython.display import HTML



import json
data_path = "data/"
supported_extension = ".jsonl"
raports_dir = "raports/"

data_files = [file_name for file_name in listdir(data_path) if isfile(data_path + file_name)]
data_jsonl = [file_name for file_name in data_files if file_name.endswith(supported_extension)]

atributes = {}
atributes_stats = []

for file in data_jsonl:
    file_loaded = pd.read_json(data_path+file, lines=True)
    data_frame = file_loaded
    print(f"Analyzing file {file}")
    print(data_frame.info())
    print("Null values info:")
    print(data_frame.isnull().sum())
    if file == "artists.jsonl":
        missing_artists_id = data_frame.loc[data_frame["id"] == -1]
        missing_artists_id.to_json(raports_dir+'missing_artists_id.jsonl', orient='records', lines=True)
        artists_without_genres = data_frame.loc[data_frame["genres"].isnull()]
        artists_without_genres.to_json(raports_dir+'artists_without_genres.jsonl', orient='records', lines=True)
    elif file == "users.json":
        pass
    elif file == "tracks.jsonl":
        missing_tracks_id = data_frame.loc[data_frame["id"].isnull()]
        missing_tracks_id.to_json(raports_dir+'missing_tracks_id.jsonl', orient='records', lines=True)
        missing_artists_for_track = data_frame.loc[data_frame["id_artist"].isnull()]
        missing_artists_for_track.to_json(raports_dir+'missing_artists_for_track.jsonl', orient='records', lines=True)
        missing_title_for_track = data_frame.loc[data_frame["name"].isnull()]
        missing_title_for_track.to_json(raports_dir+'missing_title_for_track.jsonl', orient='records', lines=True)
    elif file == "sessions.jsonl":
        sessions_without_user = data_frame.loc[data_frame["user_id"].isnull()]
        sessions_without_user.to_json(raports_dir+'sessions_without_user.jsonl', orient='records', lines=True)
        sessions_without_track = data_frame.loc[data_frame["event_type"] != "advertisment"].loc[data_frame["track_id"].isnull()]
        sessions_without_track.to_json(raports_dir+'sessions_without_track.jsonl', orient='records', lines=True)
        sessions_without_event_type = data_frame.loc[data_frame["event_type"].isnull()]
        sessions_without_event_type.to_json(raports_dir+'sessions_without_event_type.jsonl', orient='records', lines=True)
    else:
        pass