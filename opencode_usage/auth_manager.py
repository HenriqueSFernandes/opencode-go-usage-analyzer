import requests

from .auth import is_authenticated
from .client import build_usage_url, fetch_usage_page
from .parser import parse_response
from .prompt import prompt_auth_token, prompt_workspace_id
from .session import load_session, save_session


def _credentials_are_valid(workspace_id: str, auth_token: str) -> bool:
    url = build_usage_url(workspace_id)

    try:
        response = fetch_usage_page(url, auth_token)
    except requests.exceptions.RequestException:
        return False

    soup = parse_response(response.text)
    return is_authenticated(soup)


def get_credentials(remember: bool) -> tuple[str, str] | None:
    if remember:
        saved_session = load_session()
        if saved_session:
            workspace_id, auth_token = saved_session
            if _credentials_are_valid(workspace_id, auth_token):
                return workspace_id, auth_token
            print(
                "Saved session is invalid or expired. Please enter fresh credentials."
            )

    while True:
        workspace_id = prompt_workspace_id()
        auth_token = prompt_auth_token()

        if _credentials_are_valid(workspace_id, auth_token):
            if remember:
                save_session(workspace_id, auth_token)
            return workspace_id, auth_token

        print("Authentication failed. Please check your workspace ID and auth token.")
