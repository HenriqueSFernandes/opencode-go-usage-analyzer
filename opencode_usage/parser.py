import re

from bs4 import BeautifulSoup

from .models import UsageEntry


USAGE_PATTERN = re.compile(
    r"(Rolling|Weekly|Monthly) Usage(\d+%)Resets in(.*?)(?=Rolling|Weekly|Monthly|$)"
)


def parse_response(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def extract_usage(soup: BeautifulSoup | None) -> list[UsageEntry]:
    if soup is None:
        return []

    usage_div = soup.find("div", attrs={"data-slot": "usage"})
    if not usage_div:
        return []

    usage_text = usage_div.get_text(strip=True)
    matches = USAGE_PATTERN.findall(usage_text)

    usage_entries: list[UsageEntry] = []
    for usage_type, percentage, reset_time in matches:
        usage_entries.append(
            UsageEntry(
                usage_type=usage_type,
                percentage=int(percentage.replace("%", "")),
                resets_in=reset_time.strip(),
            )
        )

    return usage_entries
