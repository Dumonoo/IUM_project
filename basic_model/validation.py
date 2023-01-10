from data_fetcher import DataFetcher
from get_user_data import analyse_user
from model import KNNModel
from main2 import KMeanModel


def validate_model(model):
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


if __name__ == "__main__":
    model = KMeanModel()
    print("KMean:", validate_model(model))
    model = KNNModel()
    print("KNN:", validate_model(model))
