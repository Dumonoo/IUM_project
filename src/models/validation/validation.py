#!/usr/bin/env python3
from models.utils.data_fetcher import DataFetcher

from models.kmean_model import KMeanModel
from models.knn_model import KNNModel
from models.random_model import RandomModel
from models.regression_recommender import RegressionRecommender
from models.popular_model import PopularModel

data_fetcher = DataFetcher("all")


def validate_model(model):
    all_tp = 0
    all_fp = 0
    for user in range(101, 151):
        tp, fp = validate_for_user(model, user)
        if tp is None:
            continue
        all_tp += tp
        all_fp += fp
    if not (all_tp + all_fp):
        return 0
    precision = all_tp / (all_tp + all_fp)
    return precision


# def validate_for_user(model, user_id):
#     all_liked = data_fetcher.get_all_liked_by_user(user_id)
#     all_listened = data_fetcher.get_all_listened_to_by_user(user_id)
#     all_skipped = data_fetcher.get_all_skipped_by_user(user_id)
#     used = model.train(all_liked[:10], all_listened[:10], all_skipped[:10])
#     train = all_liked[:10]
#     recommended = model.recommend(train)
#     true_positive = len(
#         [track for track in recommended if track in all_listened or track in all_liked]
#     )
#     false_positive = len([track for track in recommended if track in all_skipped])
#     model.reset()
#     return true_positive, false_positive


def validate_for_user(model, user_id):
    used = model.train(user_id)
    all_liked = data_fetcher.get_all_liked_by_user(user_id)
    all_listened = data_fetcher.get_all_listened_to_by_user(user_id)
    all_skipped = data_fetcher.get_all_skipped_by_user(user_id)
    train = all_liked[:10]
    recommended = model.recommend(train)
    true_positive = len([track for track in recommended if track in all_liked])
    false_positive = len([track for track in recommended if track in all_skipped])
    model.reset()
    return true_positive, false_positive


def validate_cf():
    ...


def validate_random():
    r = []
    for seed in range(100):
        r.append(validate_model(RandomModel(seed)))
    return sum(r) / len(r)


def validate_all_models():
    models_info = {
        # "KMean": validate_model(KMeanModel()),
        # "Regression": validate_model(RegressionRecommender()),
        "KNN": validate_model(KNNModel()),
        "Random": validate_random(),
        # "Popular": validate_model(PopularModel()),
    }
    return models_info
