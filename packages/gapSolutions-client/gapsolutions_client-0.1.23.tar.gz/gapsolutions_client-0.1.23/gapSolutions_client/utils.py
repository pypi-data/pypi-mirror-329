import json
import requests
from . import logger
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Union
from .constants import INTERNAL_SERVER_ERROR_MESSAGE



@dataclass
class ApiResponse:
    message: str
    data: dict
    status: int = 200

@dataclass
class ApiErrorResponse:
    message: str
    status: int = 400


log = logger.get_logger("gap-client.utils")

def make_request(method, url, auth_token, query_params=None, json_payload=None):
    """
    Generic function to make API requests with error handling.

    :param method: HTTP method (GET, POST, PUT, DELETE)
    :param url: API endpoint
    :param auth_token: Authorization token
    :param query_params: Dictionary of query parameters (default: empty dict)
    :param json_payload: Dictionary of JSON payload for POST/PUT requests (default: None)
    :return: JSON response or ApiErrorResponse
    """
    log.debug("make_request() entry")

    if not auth_token:
        log.error("Authorization token is missing")
        return ApiErrorResponse(message="Authorization token required", status=401)

    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    query_params = query_params or {}
    try:
        response = requests.request(method, url, headers=headers, params=query_params, json=json_payload, allow_redirects=False)
        response.raise_for_status()  # Raises an exception for 4xx/5xx responses
        log.debug("make_request() exit")
        return response.json()  # Successful response
    except requests.exceptions.HTTPError as http_err:
        log.error(f"HTTP error: {http_err}")
        response_data = response.json()
        log.debug("make_request() exit")
        return ApiErrorResponse(message= response_data.get('message', 'Error occurred'), status=response.status_code if response.status_code else 500)
    
    except requests.exceptions.RequestException as req_err:
        log.error(f"Request error: {req_err}")
        log.debug("make_request() exit")

        return ApiErrorResponse(message=INTERNAL_SERVER_ERROR_MESSAGE, status=500)