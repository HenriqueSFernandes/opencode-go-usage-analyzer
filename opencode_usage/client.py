import requests


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def build_usage_url(workspace_id: str) -> str:
    return f"https://opencode.ai/workspace/{workspace_id}/go"


def fetch_usage_page(
    url: str, auth_token: str, headers: dict | None = None
) -> requests.Response:
    request_headers = headers or DEFAULT_HEADERS
    cookies = {"auth": auth_token, "oc_locale": "en"}
    response = requests.get(url, cookies=cookies, headers=request_headers, timeout=30)
    response.raise_for_status()
    return response
