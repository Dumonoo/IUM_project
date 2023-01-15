#!/usr/bin/env python3
from src.models.utils.get_user_data import get_user_sessions_info
from src.models.utils.data_loader import DataLoader
from src.models.validation.validation_new import validate_user, validate_model, validate_system, validate_user_score
from src.models.knn_model2 import KNNModel
from src.models.kmean_model2 import KMeanModel
from src.models.random_model_genres import RandomModelGenres
# Ponowna analiz danych w celu ulepszenia modeli
print("Co ma byc to bedzie")
data_object = DataLoader()

t = ['1lH6djMd9eN2xUGQgfyLD9', '4QJLKU75Rg4558f4LbDBRi', '3NcO4jGK1Opb5ea0mYLpxb', '376zCxYCHr7rSFBdz41QyE',
       '6RB9YvNyP0RZfCUcMtZELH', '2HiR73Vgzf048Qq8A9bYak', '6PHn6aXuM2FkzonGWJxY28', '6Ln4CTzBmbVUaV11ZVgYNI',
       '6GyKm6DWZqF2el8ItMfVIK', '5oTOpSNp2FOLgjUeCGKjXp']
# print(data_object.get_life(101))
# print(data_object.get_populatirty_stats())
# validate_model()
# print(data_object.get_track_popularity('4QJLKU75Rg4558f4LbDBRi'))


# Sprawdzanie popularnych poprzedniego dnia
# print(data_object.print_popular_over_sessions())

# validate_system()
# knn = KNNModel()
# rd = RandomModelGenres()
# kmean = KMeanModel()
# kmean.train()
# kmean.recommend2(102, 329)
# print("Cmon")
# knn.train()
# validate_user_score(knn, 101)
# data_object.get_user_popular_genres_in_session(102, 329, 3)
# validate_user_score(knn, 143)
# rd.recommend2(102, 329)
# print(data_object.get_user_future_sessions(102, 329))

# data_object.calcualte_estaminations()

# print(data_object.get_session_populatirty_stats())
# knn.train()
# knn.recommend2(102, 329)
# data_object.calcualte_estaminations()

# kmean = KMeanModel()
# kmean.test_elow()
validate_system()
# data_object.get_most_popular_track_in_n_days(332, 2)