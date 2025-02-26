import requests
from urllib.parse import urlencode
from ..models import SharingInput, AccessGranted, UpdateUser, ErrorReport, UserData, UserRegistration
from typing import Union
from ..utils import safe_json_request, safe_login, safe_data_request

endpoint = "share/"



def share(baseurl: str, sharing_input: SharingInput, token: str):
    uri = baseurl + f'{endpoint}'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    data = sharing_input.model_dump(exclude_unset=False)
    response = safe_json_request('POST', uri, data, headers)
    if isinstance(response, ErrorReport):
        raise ValueError(f"HTTP Status: {response.status} \nHTTP Reason: {response.reason} \nAPI Message: {response.message} \nAPI Status Code: {response.internal_status}")
    return True

def unshare(baseurl: str, sharing_input: SharingInput, token: str):
    uri = baseurl + f'{endpoint}'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    data = sharing_input.model_dump(exclude_unset=False)
    response = safe_json_request('DELETE', uri, data, headers)
    if isinstance(response, ErrorReport):
        raise ValueError(f"HTTP Status: {response.status} \nHTTP Reason: {response.reason} \nAPI Message: {response.message} \nAPI Status Code: {response.internal_status}")
    return True

