#!/usr/bin/env python3
from models.utils.data_fetcher import DataFetcher

from models.kmean_model import KMeanModel
from models.knn_model import KNNModel
from models.random_model import RandomModel
from models.popular_model import PopularModel

data_fetcher = DataFetcher("all")


def validate_model(model):
    model.train()
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


def validate_for_user(model, user_id):
    all_liked = data_fetcher.get_all_liked_by_user(user_id)
    if len(all_liked) < 20:
        return None, None
    train = all_liked[:10]
    test = all_liked[10:]
    recommended = model.recommend(train)
    true_positive = len([track for track in recommended if track in test])
    false_positive = len([track for track in recommended if track not in test])
    return true_positive, false_positive


def validate_all_models():
    models_info = {
        "KMean": validate_model(KMeanModel()),
        "KNN": validate_model(KNNModel()),
        "Random": validate_model(RandomModel()),
        "Popular": validate_model(PopularModel()),
    }
    return models_info
