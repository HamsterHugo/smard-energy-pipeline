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

def get_timestamps(
        filter_id: int,
        region: str = "DE",
        resolution: str = "quarterhour",
        print_url: bool = False
    ) -> list[int]:
    """Returns the list of valid block timestamps for the given SMARD filter.

    Each timestamp represents the start of a weekly data block (Monday at
    00:00 AM Europe/Berlin time) and can be used to query the corresponding
    time series via 'get_smard_timeseries'.

    Args:
        filter_id (int): The SMARD filter ID of the requested data category
            (e.g. 4068 for photovoltaics, 4067 for onshore wind).
        region (str): Region code. Defaults to "DE".
        resolution (str): Time resolution of the data. Available options:
            "quarterhour", "hour", "day", "week", "month", "year".
            Defaults to "quarterhour".
        print_url (bool): If True, prints the request URL for debugging.
            Defaults to False.

    Returns:
        list[int]: List of valid timestamps in milliseconds (Unix time).
            Each value marks the start of a weekly data block.

    Example:
        >>> timestamps = get_timestamps(4068)
        >>> len(timestamps)
        604
        >>> timestamps[0]
        1419807600000
    """
    url: str = f"{BASE_URL}/chart_data/{filter_id}/{region}/index_{resolution}.json"
    if print_url: print(f'Fetching: {url}')
    
    return requests.get(url).json()['timestamps']