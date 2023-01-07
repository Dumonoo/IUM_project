#!/usr/bin/env python3


import pandas as pd

users = pd.read_json("data/users.jsonl", lines=True)
sessions = pd.read_json("data/sessions.jsonl", lines=True)

# Returns all user sessions
def get_user_sessions_info(user_id):
    sessions_info = sessions.loc[sessions["user_id"] == user_id]
    sessions_info = sessions_info.loc[sessions_info['event_type'] != "advertisment"]
    return sessions_info

def get_user_sessions_list(user_id):
    sessions_info = get_user_sessions_info(user_id=user_id)
    return sessions_info.groupby(by=['session_id'], group_keys=True).apply(lambda x: x)
    # for session_id in sessions_info.groupby(by=['session_id'], group_keys=True).apply(lambda x: x):
    #     print(session_id)

def print_group_info(group):
    print(f'Session ID: {group.name}')
    print(group)
sessions_list = get_user_sessions_list(101)

print(get_user_sessions_list(user_id=101).loc[124])
# sessions_list.apply(print_group_info)
# for session_id in sessions_list:
#     print(f'Session ID: {session_id}')
    # print(group)
print("hello world")