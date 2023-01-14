#!/usr/bin/env python3
# from models.utils.data_loader import DataLoader
from src.models.utils.data_loader import DataLoader
# Info from N session and check M next session for results -> M = 0 all future sessions TODO
N_SESSIONS = 3
M_SESSIONS = 7
TOP_S = 4

data_loader = DataLoader()
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

    # input_ids, check_ids = model.data_obj.get_input_and_check_ids(user_id, n_sessions, m_sessions)
    # input_ids = ['6RB9YvNyP0RZfCUcMtZELH', '2HiR73Vgzf048Qq8A9bYak', '08Jr52g99jcHUYx9NhU0IE']
    # model.train()
    # output_ids = model.recommend(input_ids)


    ...

def validate_all_models():
    ...
    # models_info = {
    #     "KMean": validate_model(KMeanModel()),
    #     "KNN": validate_model(KNNModel()),
    #     "Random": validate_model(RandomModel()),
    #     "Popular": validate_model(PopularModel()),
    # }

    # return models_info