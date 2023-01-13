#!/usr/bin/env python3
from enum import Enum
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from datetime import datetime
import pandas as pd


from models.knn_model import KNNModel
from models.validation.validation import validate_model
from models.utils.get_user_data import analyse_user
from models.utils.data_fetcher import DataFetcher

class ModelEnum(Enum):
    KNN = "KNN"
    Random = "Random"

# Group A -> Model Random Group B -> Model KNN
users_group_A = [116, 130, 124, 138, 101, 142, 148, 144, 135, 136, 137, 122, 143, 125, 145, 107, 147, 126, 140, 146, 105, 129, 128, 103, 106]
users_group_B = [127, 115, 110, 109, 133, 119, 149, 108, 112, 114, 131, 113, 141, 118, 139, 111, 134, 117, 102, 123, 132, 104, 120, 121, 150]


app = FastAPI(title="App")
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
    if model_name is ModelEnum.KNN:
        ...
    
    if model_name is ModelEnum.Random:
        ...
    else:
        ...
        # log unknown model_name
        # Model Random 
    # return prediction

# Recommend 10 tracks playlist for given user_id for today
@app.get('/ab_recommendation/{user_id}')
def get_ab_recommendation(user_id: int):
    if user_id in users_group_A:
        ...
        # Group A -> Model Random 
    if user_id in users_group_B:
        ...
        # Group B -> Model KNN
    else:
        ...
        # log user not in group A and B
        # Group B -> Model Random 

    # return prediction

# Additional endpoints for testing purposes
# Recommend 10 tracks playlist for user_id with selected model using sessions before timestamp
@app.get('/recommendation_for_timestamp/{model_name}/{timestamp}/{user_id}')
def get_recommendation_for_timestamp(model_name: ModelEnum, user_id: int, timestamp: datetime):
    ...

# Recommend 10 tracks playlist for user_id with selected model using sessions before session_id
@app.get('/recommendation_for_session_id/{model_name}/{session_id}/{user_id}')
def get_recommendation_for_session_id(model_name: ModelEnum, user_id: int, session_id: int):
    ...

# Not needed
@app.get('/get_user_sessions/{user_id}')
def get_user_sessions_info(user_id: int):
    ...

# OLD CODE
@app.get("/recommend_to_user/{user_id}")
def recommend_to_user(user_id: int):
    liked, timestamp = analyse_user(user_id).get_n_last_liked(10)
    recommended = model.recommend(liked)
    return data_fetcher.get_songs(recommended).tolist()



