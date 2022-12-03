#!/usr/bin/env python3

from os import listdir
from os.path import isfile

import pandas as pd
import matplotlib.pyplot as plt
import json
data_path = "data/"
supported_extension = ".jsonl"
plots_dir = "data_distribution/plots/"
extra_raports_dir = "data_distribution/extra_raports/"

data_files = [file_name for file_name in listdir(data_path) if isfile(data_path + file_name)]
data_jsonl = [file_name for file_name in data_files if file_name.endswith(supported_extension)]

print(data_jsonl)
for file in data_jsonl:
    file_loaded = pd.read_json(data_path+file, lines=True)
    data_frame = file_loaded
    if file == "artists.jsonl":
        continue
        print(data_frame.info())
        print(data_frame.isnull().sum())
        # Checking id
        id_info = {}
        id_list = data_frame["id"].to_list()
        for id in id_list:
            if id not in id_info:
                id_info[id] = 1
            else:
                id_info[id] += 1

        # Checking genres
        genres_info = {}
        genres_list = data_frame["genres"].to_list()

        for artist_genres in genres_list:
            if artist_genres:
                for gen in artist_genres:
                    if gen not in genres_info:
                        genres_info[gen] = 1
                    else:
                        genres_info[gen] += 1

        # Charts for genres
        top_counter = 7
        sorted_genres = sorted(genres_info.items(), key=lambda x: x[1], reverse=True)
        genres_info = dict(sorted_genres)
        genres_df = pd.DataFrame.from_dict(genres_info, orient='index',
                       columns=['number_of'])
        # Plot of genres and their occurences among artists
        genres_df.plot(y='number_of', use_index=True)
        plt.title('Genres among artists')
        plt.xlabel('Genre name')
        plt.ylabel('Occurences')
        plt.savefig(plots_dir+'artist_genres_plot1.png')
        genres_df.plot.pie(y='number_of', use_index=True, legend=False, labels=None)
        plt.title('Genres among artists')
        plt.savefig(plots_dir+'artist_genres_pie_plot1.png')
        # Save to file list of all genres
        genres_df.to_csv(extra_raports_dir + "genres.txt", sep='\t', header=False) 
    elif file == "users.jsonl":
        continue
        # print("Data Information")
        # print(data_frame.info())
        # print()
        # print("Data Missing Values")
        # print(data_frame.isnull().sum())
        # print()
        # print("Data Description")
        # print(data_frame.describe())
        # print(data_frame["user_id"].value_counts())
        # print(data_frame.shape)
        # data_frame.hist(column="user_id", bins=50, grid=False, figsize=(12,8), zorder=2, rwidth=0.9)
        # plt.title('Users id distribution')
        # plt.xlabel('user_id')
        # plt.ylabel('Number of')
        # plt.savefig(plots_dir+'user_id_hist.png')

        # data_frame['city'].value_counts().plot(kind='bar')
        # plt.title('City distribution')
        # plt.xlabel('City')
        # plt.ylabel('Number of')
        # plt.savefig(plots_dir+'city_hist.png')

        # data_frame['street'].value_counts().plot(kind='bar')
        # plt.title('Street distribution')
        # plt.xlabel('Street')
        # plt.ylabel('Number of')
        # plt.savefig(plots_dir+'street_hist.png')

        # data_frame['premium_user'].value_counts().plot(kind='bar')
        # plt.title('Premium  users distribution')
        # plt.xlabel('State')
        # plt.ylabel('Number of')
        # plt.savefig(plots_dir+'premium_hist.png')
        # print(data_frame['premium_user'].value_counts())

        # Checking genres
        # genres_info = {}
        # genres_list = data_frame["favourite_genres"].to_list()

        # for user_fav in genres_list:
        #     if user_fav:
        #         for gen in user_fav:
        #             if gen not in genres_info:
        #                 genres_info[gen] = 1
        #             else:
        #                 genres_info[gen] += 1
        # sorted_genres = sorted(genres_info.items(), key=lambda x: x[1], reverse=True)
        # genres_info = dict(sorted_genres)
        # genres_df = pd.DataFrame.from_dict(genres_info, orient='index',
        #                columns=['number_of'])
        # genres_df.plot(kind='bar')
        # plt.title('Favorite genres - users')
        # plt.xlabel('Genre')
        # plt.ylabel('Number of')
        # plt.savefig(plots_dir+'fav_genre_usr_hist.png')
        # genres_df.plot.pie(y='number_of', use_index=True, legend=False)
        # plt.title('Favorite genres among users')
        # plt.savefig(plots_dir+'fav_genres_for_users.png')
        # print(genres_df)
        # data_frame['name'].value_counts().hist()
        
    elif file == "tracks.jsonl":
        continue
        print(data_frame.info())
        print(data_frame.isnull().sum())
    elif file == "sessions.jsonl":
        print(data_frame.info())
        print(data_frame.isnull().sum())
        # data_frame['session_id'].value_counts().plot(kind='bar')
        # plt.title('Session id distribution')
        # plt.xlabel('State')
        # plt.ylabel('Number of')
        # plt.savefig(plots_dir+'session_id_hist.png')
        # print(data_frame['session_id'].value_counts())
        data_frame['user_id'].value_counts().plot(kind='bar')
        plt.title('User_id in sessions distribution')
        plt.xlabel('State')
        plt.ylabel('Number of')
        plt.savefig(plots_dir+'user_id_ses__hist.png')
        print(data_frame['user_id'].value_counts())
    plt.show()