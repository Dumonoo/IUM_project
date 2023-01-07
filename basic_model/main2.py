#!/usr/bin/env python3
# K-Mean content-base filtering algorithm

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import seaborn as sns
import os
from datetime import datetime
from collections import defaultdict

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

import plotly.express as px 

def get_year(str_date):
    data_obj = None
    if len(str_date) == 4:
        data_obj = datetime.strptime(str_date, "%Y")
    elif len(str_date) == 7:
        data_obj = datetime.strptime(str_date, "%Y-%m")
    else:
        data_obj = datetime.strptime(str_date, "%Y-%m-%d")
    return data_obj.year

tracks = pd.read_json("data/tracks.jsonl", lines=True)
# Add additional columns
tracks['year'] = tracks.apply(lambda x: get_year(x["release_date"]), axis=1)
additional_columns = ['year']
sound_features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'valence']

used_columns = ['popularity', 'duration_ms', 'explicit', 'danceability', 
                'energy', 'key', 'loudness', 'speechiness', 'acousticness',
                'instrumentalness', 'liveness', 'valence', 'tempo', 'year']

example = ['0uybt73QFXaLCoxuVf6fhm', '6SQfZKwce4nGuMwrcVwK8C', '6VFimaHK7Mv5GO5NrqGYu1', '4yORNsoYe4XnK99EXhKhWB', '2D1hlMwWWXpkc3CZJ5U351', '466cKvZn1j45IpxDdYZqdA']

song_cluster_pipeline = Pipeline([('scaler', StandardScaler()), 
                                  ('kmeans', KMeans(n_clusters=14, 
                                   verbose=2))],verbose=True)
to_normalize = tracks.select_dtypes(np.number)
X = tracks.select_dtypes(np.number)
song_cluster_pipeline.fit(X)

def get_track_data(track_id, track_data):
    return track_data.loc[track_data['id'] == track_id]

def get_mean_vector(track_list_ids, tracks_data):
    tracks_vectors = []
    for track_id in track_list_ids:
        track_data = get_track_data(track_id, tracks_data)
        # Check if track exists in track_data
        track_vector = tracks_data[used_columns].values
        tracks_vectors.append(track_vector)
    
    tracks_matrix = np.array(list(tracks_vectors))
    return np.mean(tracks_matrix, axis=0)

def flatten_dict_list(dict_list):     
    flattened_dict = defaultdict()
    for key in dict_list[0].keys():
        flattened_dict[key] = []
    
    for dictionary in dict_list:
        for key, value in dictionary.items():
            flattened_dict[key].append(value)
            
    return flattened_dict

def recomend_n_songs(track_list, track_data, n_songs=10):
    metadata_columns = ['id', 'name', 'year']

    tracks_center = get_mean_vector(track_list, track_data)
    
    scaler = song_cluster_pipeline.steps[0][1]
    scaled_data = scaler.transform(track_data[used_columns])
    print(len(tracks_center.reshape(1, -1)))
    scaled_track_center = scaler.transform(tracks_center)
    scaled_track_center = scaler.transform(tracks_center.reshape(1, -1))
    distances = cdist(scaled_track_center, scaled_data, 'cosine')
    index = list(np.argsort(distances)[:, :n_songs][0])
    rec_songs = track_data.iloc[index]
    # rec_songs = rec_songs[~rec_songs['name'].isin(track_dict['name'])]
    return rec_songs[metadata_columns].to_dict(orient='records')
    print("DONE")
    pass     
print(tracks.columns)

# print(data_by_year['year'])

print("hello world!")
# print(get_track_data("0uybt73QFXaLCoxuVf6fhm", tracks))
print(recomend_n_songs(example, tracks))




# fig = px.line(data_by_year, x='year', y=sound_features)
# fig.show()
# print(tracks.loc[tracks["explicit"] == 1])
# data_by_year = tracks.groupby('year').mean()
# data_by_year = data_by_year.unstack(level=0)
# mean_values = tracks[sound_features.extend(additional_columns)].groupby('year').mean()
# mean_data = pd.DataFrame(mean_values)
# print(mean_data)
# fig = px.line(mean_data, x='year', y=sound_features)
# mean_data = pd.DataFrame(mean_values, columns=['mean'])
# mean_data['year'] = tracks['year'].unique()
# fig = px.line(mean_data, x='year', y='mean')
# fig = px.line(tracks, x='year', y=sound_features)
# fig.show()
# print(tracks['release_date'])