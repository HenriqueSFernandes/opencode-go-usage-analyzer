from dataclasses import dataclass


@dataclass(frozen=True)
class UsageEntry:
    usage_type: str
    percentage: int
    resets_in: str
