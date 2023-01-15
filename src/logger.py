#!/usr/bin/env python3
import os.path
import json
from datetime import datetime
from typing import List
from uuid import UUID

LOG_FILE_PATH = "logs"
LOG_FILE_NAME_TXT = "recomendations.log"
LOG_FILE_NAME_JSON = "recomendations.json"
LOG_FILE_FULL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), LOG_FILE_PATH)

TYPE = "INFO"

def get_timestamp():
    current_time = datetime.now()
    formated_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    return formated_time

# Prepere message to be written to log file
def prepare_log_message(user_id:int, recommended_tracks: List[UUID], model_name: str, extra_info: str = None, log_type: str = "INFO"):
    message_str = f"{get_timestamp()} {log_type} - MODEL: {model_name} USER_ID: {user_id} RECOMENDED_TRACKS: {recommended_tracks}"
    if extra_info:
        message_str += f" EXTRA_INFO: {extra_info}"
    return message_str

# Prepere message to be written to log file in json format
def prepare_log_message_json(user_id:int, recommended_tracks: List[UUID], model_name: str, extra_info: str = None, log_type: str = "INFO"):
    message_json = {"timestamp": get_timestamp(), "level": log_type, "model": model_name, "user_id": user_id, "recommended_tracks": recommended_tracks}
    if extra_info:
        message_json["extra_info"] = extra_info
    return message_json

def prepere_log_error(error: str, log_type: str = "ERROR", user_id: int = None):
    message_str = f"{get_timestamp()} {log_type} - ERROR: {error}"
    if user_id:
        message_str += f" USER_ID: {user_id}"
    return message_str

def prepere_log_error_json(error: str, log_type: str = "ERROR", user_id: int = None):
    message_json = {"timestamp": get_timestamp(), "level": log_type,  "error": error}
    if user_id:
        message_json["user_id"] = user_id
    return message_json

# Called from api to begin loggin process
def log_info(user_id:int, recommended_tracks: List[UUID], model_name: str , is_AB = False):
    if is_AB:
        save_log_to_file(prepare_log_message(user_id, recommended_tracks, model_name, "TEST-A/B"))
        save_log_to_json_file(prepare_log_message_json(user_id, recommended_tracks, model_name, "TEST-A/B"))
    else:
        save_log_to_file(prepare_log_message(user_id, recommended_tracks, model_name))
        save_log_to_json_file(prepare_log_message_json(user_id, recommended_tracks, model_name))

def log_error(log_error_message: str, user_id: int = None):
    save_log_to_file(prepere_log_error(log_error_message, user_id=user_id))
    save_log_to_json_file(prepere_log_error_json(log_error_message, user_id=user_id))

def save_log_to_file(message, file_name = LOG_FILE_NAME_TXT):
    with open(f"{LOG_FILE_FULL_PATH}/{file_name}", mode="a") as log_file:
        log_file.write(message)
        log_file.write("\n")
        log_file.close()
    return

def save_log_to_json_file(message_json, file_name = LOG_FILE_NAME_JSON):
    with open(f"{LOG_FILE_FULL_PATH}/{file_name}", mode="a") as log_file:
        json.dump(message_json, log_file)
        log_file.write(',\n')
        log_file.close()

# Example usage
# log_message(101, ["123e4567-e89b-12d3-a456-426614174000", "123e4567-e89b-12d3-a456-426614174000"], "RANDOM", True)
