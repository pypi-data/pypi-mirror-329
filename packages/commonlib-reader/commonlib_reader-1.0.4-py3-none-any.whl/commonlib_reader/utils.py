import json
from typing import Dict, List
from urllib.parse import urljoin

import requests
from msal_bearer import BearerAuth, get_user_name


def get_library_names():
    url = urljoin(get_api_url(), "api/Library/NameList")
    library_names = get_json(url=url)
    library_names.sort()
    return library_names


def get_disciplines():
    return get_code("Discipline")


def get_code(code: str, scope: str = None, name: str = None):
    params = {}
    if scope is not None:
        params["scope"] = scope

    if name is not None:
        params["name"] = name
    return get_code_param(code=code, params=params)


def get_code_param(code, params=None):
    if params is None:
        params = {}

    url = urljoin(get_api_url(), f"api/Code/{code}")
    return get_json(url, params=params)


def query_sql(sql: str):
    return post_sql(sql=sql, take=0, skip=0)


def get_api_url() -> str:
    """Get base url to api

    Returns:
        str: Base url to api
    """
    return "https://commonlibapi.equinor.com/"


def get_auth() -> BearerAuth:
    """Get Bearerauth object including token for accessing api.

    Returns:
        BearerAuth: Object with access token for api.
    """
    tenantID = "3aa4a235-b6e2-48d5-9195-7fcf05b459b0"
    clientID = "728cfddd-b8e9-4ed7-b9a3-8f2fd5b8e79a"
    scopes = ["37d598fc-da0f-46bd-949f-7107918d47a5/user_impersonation"]
    auth = BearerAuth.get_auth(
        tenantID=tenantID,
        clientID=clientID,
        scopes=scopes,
        username=f"{get_user_name()}@equinor.com",
    )

    return auth


def get_json(url: str, params=None) -> list:
    """Get json from api endpoint

    Args:
        url (str): Url to api endpoint to get.
        params (dict, optional): Dictionary of parameters to pass. Defaults to None.

    Returns:
        list: List of response from api
    """
    response = requests.get(url, auth=get_auth(), params=params)
    # response.raise_for_status()
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            print(
                f"Warning: {str(url)} returned successfully, but not with a valid json response"
            )
    else:
        print(f"Warning: {str(url)} returned status code {response.status_code}")

    return []


def post_sql(sql: str, take: int = 100, skip: int = 0) -> list:
    """Get json from api/sql endpoint accepting sql queries.

    Args:
        sql (str): SQL query to run
        take (int, optional): Number of results to return. Defaults to 100.
        skip (int, optional): Number of results to skip. Defaults to 0.

    Returns:
        list: List of response from api
    """
    url = urljoin(get_api_url(), "api/sql")
    response = requests.post(
        url=url, json={"query": sql, "take": take, "skip": skip}, auth=get_auth()
    )
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            print(
                f"Warning: {str(url)} returned successfully, but not with a valid json response"
            )
    else:
        print(f"Warning: {str(url)} returned status code {response.status_code}")

    return []


def attributes_list_to_dict(attribute_list: List[Dict]) -> Dict:
    """Convert list of attributes typically returned from commonlib to a normal dictionary.

    Args:
        attribute_list (List[Dict]): List of attributes

    Returns:
        Dict: Dictionary with attribute definitionName as keys.
    """
    d = {}
    for r in attribute_list:
        try:
            d[r["definitionName"]] = r["displayValue"]
        except:
            pass

    return d
