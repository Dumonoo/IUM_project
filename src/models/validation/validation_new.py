#!/usr/bin/env python3
# from models.utils.data_loader import DataLoader
from src.models.utils.data_loader import DataLoader
from typing import List
from src.models.random_model_genres import RandomModelGenres
from src.models.knn_model2 import KNNModel

# Info from N session and check M next session for results -> M = 0 all future sessions TODO
N_SESSIONS = 3
M_SESSIONS = 30
TOP_S = 4

data_loader = DataLoader()

def validate_system():
    # For Each Model ...
    # For each user ...
    knn = KNNModel()
    rd = RandomModelGenres()
    model = rd
    for user in range(101, 151):
        score_avg = validate_user_score(model, user)
        # print(f"User: {user} - Avg.Score: {score_avg}")

def validate_user_score(model, user_id):
    
    # user_sessions = data_loader.get_user_sessions_with_estimations(user_id)
    session_order = data_loader.get_session_order(user_id)
    # We split data into 3 categories user_history, train_data, test_data 20%,20%,60%
    history_prc = 0.2 ; train_prc = 0.2 ; test_prc = 0.6
    user_history = session_order[:int(len(session_order) * history_prc)]
    user_train = session_order[int(len(session_order) * history_prc) : int(len(session_order) * (history_prc + train_prc))]
    test_data = session_order[int(len(session_order) * (history_prc + train_prc)):]
    # print(f"USER: {user_id} {user_history} {user_train} {test_data}")

    tests_counter = 0
    user_score = 0
    for session_id in user_train:
        tests_counter += 1
        recommendations_ids = model.recommend(user_id, session_id)
        user_score += check_recommendations(recommendations_ids, user_id, session_id)
        # print(session_id)
    print(f"User {user_id} tests_counter{tests_counter}")
    return user_score/tests_counter, tests_counter


    ...
def check_recommendations(recommendations: List[str], user_id: int, session_id: int):
    score = 0
    if len(recommendations) != 10:
        print(f"WARNING User {user_id} Session {session_id} LESS THEN 10 tracks {len(recommendations)}")
        
    future_sessions = data_loader.get_user_future_sessions(user_id, session_id)
    for index, session in future_sessions.iterrows():
        if session['track_id'] in recommendations and session['event_type'] == 'play':
            score += 1
        if session['track_id'] in recommendations and session['event_type'] == 'like':
            score += 1.5
    return score/len(recommendations)

    # Calculate score over future of user sessions
    ...
def recommend(user_id, session_id):
    ... # mozna zamiast przekazywania session_data_with_marks obliczyc to dla wszysktich userow przy logowaniu 
    # Na podstawie user_id odnajdujemy sesjie uzytkownika
    # Wybieramy inreresujaca nas sessje 
    # oceniamy i wybieramy inreresujace nas id
    # z modelu wyciagamy liste id podobnych do tych utworow
    # sortujemy je wzgledem popularnosci i dajemy najpopularniejsze


# def validate_model(model):
#     model.train()
#     all_tp = 0
#     all_fp = 0
#     for user in range(101, 151):
#         tp, fp = validate_for_user(model, user)
#         if tp is None:
#             continue
#         all_tp += tp
#         all_fp += fp
#     if not (all_tp + all_fp):
#         return 0
#     precision = all_tp / (all_tp + all_fp)
#     return precision





















# test for every sessions po kolei zaczynajc od N_SESSIONS az do M_SESSIONS od konca
def validate_user(model, user_id: int):
    session_info = data_loader.get_sessions_list_in_order(user_id)
    tests = 0
    evalueation_score = 0
    for i in range(N_SESSIONS, len(session_info)- M_SESSIONS):
        tests += 1
        n_sess = session_info[i-N_SESSIONS:i]
        m_sess = session_info[i:i+M_SESSIONS]
        input_ids, check_ids = data_loader.get_input_and_check_ids(user_id, n_sess, m_sess)
        input_ids = input_ids['track_id'].values[:TOP_S]
        model.train()
        recomended_ids = model.recommend(input_ids)
        mark = data_loader.calcate_score(recomended_ids, check_ids)
        evalueation_score += mark

    return evalueation_score/tests

def validate_user_new(model, user_id: int):
    session_info = model.data_obj.get_sessions_list_in_order(user_id)
    session_mark = model.data_obj.get_user_sessions_with_estimations(user_id)
    model.train()
    tests = 0
    evalueation_score = 0
    for i in range(N_SESSIONS, len(session_info)- M_SESSIONS):
        tests += 1
        n_sess = session_info[i-N_SESSIONS:i]
        m_sess = session_info[i:i+M_SESSIONS]
        input_ids, check_ids = model.data_obj.get_input_and_check_ids_new(user_id, n_sess, m_sess, session_mark)
        recomended_ids = model.recommend(input_ids['track_id'].values, user_id)
        mark = model.data_obj.calcate_score(recomended_ids, check_ids)
        evalueation_score += mark
        print(mark)
        # print(n_sess, m_sess)
    print("score: ", evalueation_score/tests)


def validate_session_based(model, user_id):
    session_info = model.data_obj.get_sessions_list_in_order(user_id)
    session_mark = model.data_obj.get_user_sessions_with_estimations(user_id)
    model.train()
    tests = 0
    evalueation_score = 0
    for i in session_info:
        tests += 1
        n_sess = [i]
        m_sess = [x for x in session_info if x != i]
        input_ids, check_ids = model.data_obj.get_input_and_check_ids_new(user_id, n_sess, m_sess, session_mark)
        recomended_ids = model.recommend(input_ids['track_id'].values, user_id)
        mark = model.data_obj.calcate_score(recomended_ids, check_ids)
        evalueation_score += mark
        # print(mark)
        # print(n_sess, m_sess)
    print("score: ", evalueation_score, evalueation_score/tests)
    # ...

def validate_track_based(model, user_id):
    session_info = model.data_obj.get_sessions_list_in_order(user_id)
    session_mark = model.data_obj.get_user_sessions_with_estimations(user_id)
    print(len(session_mark['track_id']))

def validate_model():
    model = RandomModelGenres()
    model2 = KNNModel()
    # model2.train()
    # user_id = 101
    # t = ['1lH6djMd9eN2xUGQgfyLD9', '4QJLKU75Rg4558f4LbDBRi', '3NcO4jGK1Opb5ea0mYLpxb', '376zCxYCHr7rSFBdz41QyE',
    #    '6RB9YvNyP0RZfCUcMtZELH', '2HiR73Vgzf048Qq8A9bYak']
    # validate_session_based(model, 103)
    validate_session_based(model2, 103)
    # print(model2.recommend(t,user_id))
    # print(validate_user_new(model, _user_id))
    # validate_session_based(model, _user_id)
    # validate_track_based(model, _user_id)




def validate_all_models():
    ...
    # models_info = {
    #     "KMean": validate_model(KMeanModel()),
    #     "KNN": validate_model(KNNModel()),
    #     "Random": validate_model(RandomModel()),
    #     "Popular": validate_model(PopularModel()),
    # }

    # return models_info