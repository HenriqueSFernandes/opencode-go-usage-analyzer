from bs4 import BeautifulSoup


def is_authenticated(soup: BeautifulSoup | None) -> bool:
    if soup is None:
        return False
    google_link = soup.find(
        lambda tag: tag.name == "a" and "Continue with Google" in tag.get_text()
    )
    return google_link is None
