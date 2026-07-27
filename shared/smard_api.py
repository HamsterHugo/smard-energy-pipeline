import datetime

import requests
from typing import TypedDict

from config import BASE_URL

# Define classes
class MetaData(TypedDict):
    version: int
    created: int

class SmardBlock(TypedDict):
    meta_data: MetaData
    series: list[list[int | float | None]]

def is_current_week(timestamp_ms: int) -> bool:
    """Returns True if the given timestamp falls within the current week.
    
    Args:
        timestamp_ms (int): Unix timestamp in milliseconds.
    
    Returns:
        bool: True if the timestamp is within the current week.
    """
    block_start = datetime.datetime.fromtimestamp(
        timestamp_ms / 1000,
        tz=datetime.timezone.utc
    )
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    return (now - block_start).days < 7