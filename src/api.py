#!/usr/bin/env python3
from enum import Enum
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from datetime import datetime
import pandas as pd
from logger import log_info, log_error
from models.validation.validation import validate_all_models
from models.knn_model import KNNModel
from models.random_model import RandomModel
from models.validation.validation import validate_model
from models.utils.get_user_data import analyse_user
from models.utils.data_fetcher import DataFetcher

class ModelEnum(Enum):
    KNN = "KNN"
    Random = "Random"

# Group A -> Model Random Group B -> Model KNN
users_group_A = [116, 130, 124, 138, 101, 142, 148, 144, 135, 136, 137, 122, 143, 125, 145, 107, 147, 126, 140, 146, 105, 129, 128, 103, 106]
users_group_B = [127, 115, 110, 109, 133, 119, 149, 108, 112, 114, 131, 113, 141, 118, 139, 111, 134, 117, 102, 123, 132, 104, 120, 121, 150]


app = FastAPI(title="Recomenndation_API")

# Model preparation
base_model = RandomModel()
base_model.train()
target_model = KNNModel()
target_model.train()

model = KNNModel()
model.train()

metadata_columns = ["id", "name", "year"]
data_fetcher = DataFetcher(metadata_columns)


@app.get("/")
def root(request: Request):
    html = f"<html><body><h1><a href='{request.url._url}docs'>Strona docs dla mikroserwisu</a></h1></body></html>"
    return HTMLResponse(html)

# Main endpoints
# Recommend 10 tracks playlist for given user_id for today with selected model
@app.get('/recommendation/{model_name}/{user_id}')
def get_recommendation(model_name: ModelEnum, user_id: int):
    # TODO change this to function with will return information ready for model
    ids, timestamp = analyse_user(user_id).get_n_last_liked(10)
    recommended = []
    if model_name is ModelEnum.KNN:
        recommended = target_model.recommend(ids)
    
    if model_name is ModelEnum.Random:
        recommended = base_model.recommend(ids)
    else:
        # Model Random 
        log_error(f"Uknown model {model_name.name}")
        recommended = base_model.recommend(ids)

    recommended_list = data_fetcher.get_songs(recommended).tolist()
    log_info(user_id=user_id, recommended_tracks=recommended_list, model_name=model_name.name)
    return recommended_list

# Recommend 10 tracks playlist for given user_id for today
@app.get('/ab_recommendation/{user_id}')
def get_ab_recommendation(user_id: int):
    # TODO change this to function with will return information ready for model
    ids, timestamp = analyse_user(user_id).get_n_last_liked(10)
    recommended = []
    model_name = ""
    if user_id in users_group_A:
        # Group A -> Model Random 
        recommended = base_model.recommend(ids)
        model_name = ModelEnum.Random
    if user_id in users_group_B:
        # Group B -> Model KNN
        recommended = target_model.recommend(ids)
        model_name = ModelEnum.KNN
    else:
        # UNKOWN Group -> Model Random 
        log_error("The given user is not in any of the groups a and b", user_id=user_id)
        model_name = ModelEnum.Random
        recommended = base_model.recommend(ids)

    recommended_list = data_fetcher.get_songs(recommended).tolist()
    log_info(user_id=user_id, recommended_tracks=recommended_list, model_name=model_name.name, is_AB=True)
    return recommended_list    


# Additional endpoints for testing purposes
# Recommend 10 tracks playlist for user_id with selected model using sessions before timestamp
@app.get('/recommendation_for_timestamp/{model_name}/{timestamp}/{user_id}')
def get_recommendation_for_timestamp(model_name: ModelEnum, user_id: int, timestamp: datetime):
    ...

# Recommend 10 tracks playlist for user_id with selected model using sessions before session_id
@app.get('/recommendation_for_session_id/{model_name}/{session_id}/{user_id}')
def get_recommendation_for_session_id(model_name: ModelEnum, user_id: int, session_id: int):
    ...

# Validate both all models and return infomation about them
@app.get('/validate_models/')
def validate_models():
    return validate_all_models()





