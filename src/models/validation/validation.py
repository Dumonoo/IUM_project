#!/usr/bin/env python3
from models.utils.get_user_data import analyse_user
from models.kmean_model import KMeanModel
from models.knn_model import KNNModel
from models.random_model import RandomModel
from models.popular_model import PopularModel


def validate_model(model):
    print("Stating validation")
    model.train()
    all_rates = []
    for user in range(101, 151):
        rate = validate_for_user(model, user)
        if rate is None:
            continue
        all_rates.append(rate)
    return sum(all_rates) / len(all_rates)


def validate_for_user(model, user_id):
    n = 10
    userSessions = analyse_user(user_id)
    userSessions.sort_sessions_by_date()
    userSessions.all_session_list.reverse()
    liked, session_end = userSessions.get_n_first_liked(n)
    if not liked:
        return None
    recommended = model.recommend(liked)
    later_songs = userSessions.get_n_songs_listened_since(None, session_end)
    return 1 if any([song in later_songs for song in recommended]) else 0

def validate_all_models():
    models_info = {
        "KMean": validate_model(KMeanModel()),
        "KNN" : validate_model(KNNModel()),
        "Random": validate_model(RandomModel()),
        "Popular": validate_model(PopularModel())
    }
    return models_info

if __name__ == "__main__":
    print("KMean:", validate_model(KMeanModel()))
    print("KNN:", validate_model(KNNModel()))
    print("Random:", validate_model(RandomModel()))
    print("Popular:", validate_model(PopularModel()))
