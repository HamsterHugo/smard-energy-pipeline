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