from typing import Optional
import os, requests

BASE_URL = os.getenv("LOGGER_URL", "http://127.0.0.1:4800")
API_TOKEN = os.getenv("LOGGER_TOKEN", "")
APPLICATION_NAMESPACE = os.getenv("LOGGER_APPLICATION_NAMESPACE", "")

HEADERS = {"token": API_TOKEN, "Content-Type": "application/json"}

def register_log(timestamp: str, error: str, func_name: str, filename: str, line_no: int, 
                 detailed_exp: str, custom_msg: Optional[str] = None, params: Optional[str] = None):
    url = f"{BASE_URL}/register_log"
    payload = {
        "timestamp": timestamp,
        "error": error,
        "custom_msg": custom_msg,
        "func_name": func_name,
        "filename": filename,
        "line_no": line_no,
        "params": params,
        "detailed_exp": detailed_exp,
        "application_namespace": APPLICATION_NAMESPACE
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()
