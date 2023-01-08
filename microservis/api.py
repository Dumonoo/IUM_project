#!/usr/bin/env python3
from fastapi import Body, FastAPI
from datetime import datetime, time, timedelta
from typing import Union

app = FastAPI(title="App")

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/recommend_by_date/{advance_model}/{timestamp}/{user_id}")
def get_recommendation_by_time_cutoff(user_id: int, timestamp: datetime , advance_model: bool = True):
        # TODO
    return {"user_id": user_id}

@app.get("/recommend_by_session/{advance_model}/{session_id}/{user_id}")
def get_recommendation_by_session_id(user_id: int, session_id: int , advance_model: bool = True):
        # TODO
    return {"user_id": user_id}

@app.get("/recommend/{advance_model}/{session_id}/{user_id}")
def get_recommendation(user_id: int, session_id: int , advance_model: bool = True):
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
