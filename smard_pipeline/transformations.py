from os import devnull
from pathlib import Path

import pandas as pd
from rich.traceback import install
from rich.progress import track
from rich.console import Console

from smard_pipeline.config import RAW_DATA_DIR, PATH_DICT
from smard_pipeline.config import FILTERS

# Use install from rich for a better output of tracebacks
install()

# Define consols, one for the terminal and one for the logs.
console_terminal = Console()
console_log = Console(record=True, file=open(devnull, "w", encoding="utf-8"))

def merge_raw_data(category: str, subcategory: str) -> pd.DataFrame:
    """Loads all raw_data for the queries category and subcategories and merges
    all timeseries into one data frame.

    Args:
        category (str): Top level category from FILTERS.
        subcategory (str): Subcategory key within the category

    Returns:
        pd.DataFrame: Contains all merged energy data from all week blocks.
            Columns are 'timestamp' and <subcategory>.
    """
    # Check for valid arguments.
    if category not in FILTERS:
        console_terminal.log(
            f"[bold bright_red][ERROR][/] Unknown category: '{category}'"
        )
        console_terminal.log(
            f"[cyan][INFO][/] Available categories: {list(FILTERS.keys())}"
        )
        return
    
    if subcategory not in FILTERS[category]:
        console_terminal.log(
            f"[bold bright_red][ERROR][/] Unknown subcategory: '{subcategory}'"
        )
        console_terminal.log(
            f"[cyan][INFO][/] Available subcategories: "
            f"{list(FILTERS[category].keys())}"
        )
        return

    INPUT_DIR: Path = RAW_DATA_DIR / PATH_DICT[category]