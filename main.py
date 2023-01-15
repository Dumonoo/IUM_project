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

validate_system()
# data_object.get_most_popular_track_in_n_days(332, 2)