from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from models.utils.data_fetcher import DataFetcher
from models.regression_recommender import RegressionRecommender, RandomRegression


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
    return sum(bis) / len(bis)


if __name__ == "__main__":
    fetcher = DataFetcher("all")
    data = {user: fetcher.read_avg_listen(user) for user in range(101, 151)}
    print('Docelowe:', validate(data, False))
    print('Bazowe:', validate(data, True))
