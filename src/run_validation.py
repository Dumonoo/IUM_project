from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from models.validation.validation import validate_all_models
from models.utils.data_fetcher import DataFetcher
from models.utils.data_loader import DataLoader
from models.cosine_model import CosineModel
from models.cf_model import CFModel
from models.regression_recommender import RegressionRecommender, RandomRegression
from models.random_model import RandomModel
from models.class_knn_model import KNNClassifierModel
import random


def validate_knn_class():
    fetcher = DataFetcher("all")
    model = KNNClassifierModel()
    user = 101
    rated = fetcher.get_all_rated(user)
    data = fetcher.get_training_data(user)
    data = data.merge(rated, left_on="id", right_on="track_id")
    train, test = train_test_split(data, test_size=0.5, shuffle=False)
    model.train(train)
    prediction = model.predict(test)
    result = prediction.merge(test[["id", "event_type"]])
    tp, fp, tn = 0, 0, 0
    for id, prediction, label in result.values:
        match prediction, label:
            case "like", "like":
                tp += 1
            case "like", "skip":
                fp += 1
            case _, _:
                ...
    print(tp / (tp + fp))


def validate(data, base=False):
    all_errors = []
    bis = []
    for user in range(101, 151):
        X, y = data[user]
        if len(X) < 10 or len(y) < 10:
            continue
        model = RandomRegression() if base else RegressionRecommender()
        train_X, test_X, train_y, test_y = train_test_split(
            X, y, test_size=0.2, shuffle=False
        )
        model.train(train_X, train_y)
        prediction = model.predict(test_X)
        all_errors.append(mean_squared_error(test_y, prediction))
        pred_and_test = list(zip(prediction, test_y))
        pred_and_test = sorted(pred_and_test, key=lambda x: x[0])
        bis.append(
            len([t for p, t in pred_and_test[-10:] if p >= 0.75 and t >= 0.75])
            / len(list(pred_and_test[:10])),
        )
    print("Base:" if base else "Model:")
    print("MAE:", sum(all_errors) / len(all_errors))
    print("BIS:", sum(bis) / len(bis))


if __name__ == "__main__":
    fetcher = DataFetcher("all")
    data = {user: fetcher.read_avg_listen(user) for user in range(101, 151)}
    validate(data, False)
    validate(data, True)
    # validate_regression()
    # validation_random_regression()

    # load = DataLoader()
    # load.get_user_sessions_with_estimations(101)
    # validate_knn_class()
    # validate_regression()

    # model.write()
    # print(model.similarities)
    # fetcher = DataFetcher("all")
    # res = fetcher.read_avg_listen(101)
    # print(res)
    # model = CFModel()
    # model.train()
    # liked = fetcher.get_all_liked_by_user(101)
    # skipped = fetcher.get_all_skipped_by_user(101)
    # recs = model.recommened(101)
    # tp = len([t for t in recs if t in liked])
    # fp = len([t for t in recs if t in skipped])
    # print(tp / (tp + fp))
    # m = RegressionRecommender()
    # m.train(101)

    # print(validate_all_models())


def validate_cosine():
    model = CosineModel()
    model.read()
    tp, fp = 0, 0
    for user in range(50, 151):
        model.limit_to_user(user)
        recs = model.recommend_to_user(user)
        liked = model.fetcher.get_all_liked_by_user(user)
        listened = model.fetcher.get_all_listened_to_by_user(user)
        skipped = model.fetcher.get_all_skipped_by_user(user)
        tp += len([t for t in recs if t in listened])
        fp += len([t for t in recs if t in skipped])
        model.unlimit()
    print(tp / (tp + fp))
