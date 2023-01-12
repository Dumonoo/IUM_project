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


app = FastAPI(title="App")
model = KNNModel()
model.train()

metadata_columns = ["id", "name", "year"]
data_fetcher = DataFetcher(metadata_columns)


@app.get("/")
def root(request: Request):
    html = f"<html><body><h1><a href='{request.url._url}docs'>Strona mikroserwisu</a></h1></body></html>"
    return HTMLResponse(html)


@app.get("/recommend_to_user/{user_id}")
def recommend_to_user(user_id: int):
    liked, timestamp = analyse_user(user_id).get_n_last_liked(10)
    recommended = model.recommend(liked)
    return data_fetcher.get_songs(recommended).tolist()


class ModelEnum(Enum):
    KNN = "KNN"
    Random = "Random"


@app.get("/recommend_by_date/{advance_model}/{timestamp}/{user_id}")
def get_recommendation_by_time_cutoff(
    user_id: int, timestamp: datetime, advance_model: bool = True
):
    # TODO
    return {"user_id": user_id}


@app.get("/recommend_by_session/{advance_model}/{session_id}/{user_id}")
def get_recommendation_by_session_id(
    user_id: int, session_id: int, advance_model: bool = True
):
    # TODO
    return {"user_id": user_id}


@app.get("/recommend/{advance_model}/{session_id}/{user_id}")
def get_recommendation(user_id: int, session_id: int, advance_model: bool = True):
    # TODO
    return {"user_id": user_id}


@app.get("/user_sessions/{user_id}")
def get_user_sessions_info(user_id: int):
    # TODO
    return {"user_id": user_id}


@app.get("/get_user_info")
def get_user_sessions_info():
    # TODO
    return {"user_id": "yes"}
