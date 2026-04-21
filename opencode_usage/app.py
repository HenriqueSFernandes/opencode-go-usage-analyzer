import requests

from .auth_manager import get_credentials
from .auth import is_authenticated
from .client import build_usage_url, fetch_usage_page
from .parser import extract_usage, parse_response
from .render import print_usage
from .session import clear_session


def logout() -> None:
    if clear_session():
        print("Session cleared.")
        return
    print("No saved session found.")


def run(remember: bool = True) -> None:
    credentials = get_credentials(remember=remember)
    if credentials is None:
        print("Could not get valid credentials.")
        return
    workspace_id, auth_token = credentials

    url = build_usage_url(workspace_id)

    try:
        response = fetch_usage_page(url, auth_token)
    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {error}")
        return

    soup = parse_response(response.text)

    if not is_authenticated(soup):
        print("User is not authenticated.")
        return

    usage_data = extract_usage(soup)
    if usage_data:
        print_usage(usage_data)
        return

    print("Could not extract usage data.")
