#!/usr/bin/env python3

from os import listdir
from os.path import isfile

import pandas as pd

from sklearn.metrics.pairwise import sigmoid_kernel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing

data_path = "data/"
supported_extension = ".jsonl"
raports_dir = "raports/"

data_files = [file_name for file_name in listdir(data_path) if isfile(data_path + file_name)]
data_jsonl = [file_name for file_name in data_files if file_name.endswith(supported_extension)]

songs_dataFrame = pd.read_json("data/tracks.jsonl", lines=True)
print(songs_dataFrame.info())

choosen_columns = ['popularity', 'duration_ms', 'danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
scaler = MinMaxScaler()
normalized_df =scaler.fit_transform(songs_dataFrame[choosen_columns])

indices = pd.Series(songs_dataFrame.index, index=songs_dataFrame['id']).drop_duplicates()
print(1)
cosine = 1
# cosine = cosine_similarity(normalized_df, dense_output=True)
print(2)

def generate_recommendation(song_title, model_type=cosine):
    # Get song indices
    index=indices[song_title]
    # Get list of songs for given songs
    print(3)
    score=list(enumerate(model_type[index]))
    print(4)
    # Sort the most similar songs
    # print(len(score[1][1]))
    similarity_score = sorted(score,key = lambda x:x[1][0],reverse = True)
    print(score[1])
    # Select the top-10 recommend songs
    similarity_score = similarity_score[1:11]
    top_songs_index = [i[0] for i in similarity_score]
    # Top 10 recommende songs
    top_songs=songs_dataFrame['name'].iloc[top_songs_index]
    return top_songs

# print(generate_recommendation('Paint It, Black',cosine).values)

vec1 = [1,1,0,1,1]
vec2 = [0,1,0,1,1]
vec3 = [1,1,1,1,1]
song_id = "567gPvGfxxKoZxDKqM9tEl"
index=indices[song_id]
cosine = cosine_similarity(normalized_df, dense_output=True)
score=list(enumerate(cosine[index]))
similarity_score = sorted(score,key = lambda x:x[1],reverse = True)
similarity_score = similarity_score[1:11]
top_songs_index = [i[0] for i in similarity_score]
top_songs=songs_dataFrame['name'].iloc[top_songs_index]

# print(cosine)
print(top_songs)