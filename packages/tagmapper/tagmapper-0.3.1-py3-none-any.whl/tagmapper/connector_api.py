import json
import logging
from types import SimpleNamespace
from azure.identity import DefaultAzureCredential
import requests
from msal_bearer import BearerAuth, get_user_name


logger = logging.getLogger(__name__)

_token = ""
_user_name = ""


def set_token(token: str) -> None:
    """Setter for global property token.

    Args:
        token (str): Token to set.
    """
    global _token
    _token = token


def get_token() -> str:
    """Getter for token. Will first see if a global token has been set, then try to get a token using app registration, then last try to get via azure authentication.

    Returns:
        str: Authentication token
    """
    if _token:

        return _token

    token = get_app_token()

    if token:
        return token

    return get_az_token()


def get_az_token() -> str:
    """Getter for token uzing azure authentication.

    Returns:
        str: Token from azure authentication
    """
    credential = DefaultAzureCredential()
    databaseToken = credential.get_token("582e9f1c-1814-449b-ae6c-0cdc5fecdba2")
    return databaseToken[0]


def get_app_bearer(username: str = "") -> str:
    global _user_name

    if not username:
        if not _user_name:
            _user_name = get_user_name()
        username = _user_name
    else:
        _user_name = username

    # SHORTNAME@equinor.com -- short name shall be capitalized
    username = username.upper()  # Also capitalize equinor.com
    if not username.endswith("@EQUINOR.COM"):
        username = username + "@EQUINOR.COM"

    tenantID = "3aa4a235-b6e2-48d5-9195-7fcf05b459b0"
    clientID = "5850cfaf-0427-4e96-9813-a7874c8324ae"

    scope = ["582e9f1c-1814-449b-ae6c-0cdc5fecdba2/user_impersonation"]

    auth = BearerAuth.get_auth(
        tenantID=tenantID,
        clientID=clientID,
        scopes=scope,
        username=username,
        token_location="api_token_cache.bin",
    )
    return auth.token


def get_app_token(username: str = "") -> str:
    """Getter for token using app registration authentication.

    Args:
        username (str, optional): User name (email address) of user to get token for.

    Returns:
        str: Token from app registration
    """
    return get_app_bearer(username=username)


def get_object_from_json(text: str):
    if isinstance(text, list):
        obj = [json.loads(x, object_hook=lambda d: SimpleNamespace(**d)) for x in text]
    else:
        obj = json.loads(text, object_hook=lambda d: SimpleNamespace(**d))
    return obj


def get_api_url():
    return "https://spdapi.radix.equinor.com"


def get_json(url: str, raise_for_status=False):
    token = get_token()
    header = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=header)
    if raise_for_status:
        response.raise_for_status()

    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.warning(
                f"Warning: {str(url)} returned successfully, but not with a valid json response"
            )
    else:
        logger.warning(
            f"Warning: {str(url)} returned status code {response.status_code}"
        )

    return []
