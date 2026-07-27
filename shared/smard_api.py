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

def get_smard_timeseries(
        filter_id: int,
        timestamp: int,
        region: str = "DE",
        resolution: str = "quarterhour",
        print_url: bool = False
    ) -> SmardBlock:
    """Returns a weekly data block from the SMARD API for the given filter and
    timestamp.

    The returned block always covers exactly one week (672 entries at
    quarterhour resolution), starting on a Monday at 00:00 AM Europe/Berlin
    time. The first and last block may contain leading or trailing null values
    — the first block due to zero-padding before data availability, the last
    block due to data latency of approximately one hour.

    Args:
        filter_id (int): The SMARD filter ID of the requested data category
            (e.g. 4068 for photovoltaics, 4067 for onshore wind).
        timestamp (int): Unix timestamp in milliseconds marking the start of
            the requested weekly block (Monday at 00:00 AM Europe/Berlin).
            Use get_timestamps() to retrieve valid values.
        region (str): Region code. Defaults to "DE".
        resolution (str): Time resolution of the data. Available options:
            "quarterhour", "hour", "day", "week", "month", "year".
            Defaults to "quarterhour".
        print_url (bool): If True, prints the request URL for debugging.
            Defaults to False.

    Returns:
        dict: A weekly data block with two keys:
            meta_data (dict): Metadata with two keys:
                version (int): API version number.
                created (int): Unix timestamp in milliseconds of the last
                    update.
            series (list[list]): List of 672 entries (at quarterhour
                resolution). Each entry is a two-element list:
                    [timestamp (int), value (float | None)]
                where timestamp is Unix time in milliseconds and value is
                the measured quantity in MWh, or None if not yet available.

    Example:
        >>> timestamps = get_timestamps(4068)
        >>> block = get_smard_timeseries(4068, timestamps[-2])
        >>> len(block['series'])
        672
        >>> block['series'][0]
        [1784498400000, 0.0]
    """
    url: str = (
        f"{BASE_URL}/chart_data/{filter_id}/{region}/"
        f"{filter_id}_{region}_{resolution}_{timestamp}.json"
    )
    if print_url: print(f'Fetching: {url}')
    
    return requests.get(url).json()
