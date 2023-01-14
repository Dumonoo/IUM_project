from models.utils.data_fetcher import DataFetcher

data_fetcher = DataFetcher("all")


def validate_model(model):
    model.train()
    all_rates = []
    for user in range(101, 151):
        rate= validate_for_user(model, user)
        if rate is None:
            continue
        all_rates.append(rate)
    if not len(all_rates):
        return 0
    return sum(all_rates) / len(all_rates)


def validate_for_user(model, user_id):
    all_liked = data_fetcher.get_all_liked_by_user(user_id)
    all_listened_to = data_fetcher.get_all_listened_to_by_user(user_id)
    if len(all_liked) < 20:
        return None
    train = all_liked
    test = all_listened_to
    recommended = model.recommend(train)
    return 1 if any([song in test for song in recommended]) else 0
