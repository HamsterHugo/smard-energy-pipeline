from os import devnull
from pathlib import Path

import pandas as pd
from rich.traceback import install
from rich.console import Console
from rich.terminal_theme import MONOKAI

from smard_pipeline.config import RAW_DATA_DIR, LOGS_DIR, PATH_DICT
from smard_pipeline.config import FILTERS

# Use install from rich for a better output of tracebacks
install()

# Define consols, one for the terminal and one for the logs.
console = Console(record=True)

def merge_raw_data(category: str, subcategory: str) -> pd.DataFrame | None:
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
        console.log(
            f"[bold bright_red][ERROR][/] Unknown category: '{category}'"
        )
        console.log(
            f"[cyan][INFO][/] Available categories: {list(FILTERS.keys())}"
        )
        return
    
    if subcategory not in FILTERS[category]:
        console.log(
            f"[bold bright_red][ERROR][/] Unknown subcategory: '{subcategory}'"
        )
        console.log(
            f"[cyan][INFO][/] Available subcategories: "
            f"{list(FILTERS[category].keys())}"
        )
        return

    INPUT_DIR: Path = RAW_DATA_DIR / PATH_DICT[category]
    filter_id: int = FILTERS[category][subcategory]

    weekly_blocks: list[pd.DataFrame] = [
        pd.read_parquet(file)
        for file in RAW_DATA_DIR.glob(f'{filter_id}_*.parquet')
    ]

    if not weekly_blocks:
        console(f"[yellow][WARNING][/] No files found for {subcategory}!")
        console(f"[yellow][WARNING][/] Download raw data for {subcategory} first!")
        return None

    df: pd.DataFrame = pd.concat(weekly_blocks, ignore_index=True)
    df.columns = ['timestamps', subcategory]
    df = df.dropna()
    console(f"[bold green][SUCCESS][/] Merged raw data for {subcategory}!")
    console.save_html(
        LOGS_DIR/f'merge_log_{category}_{subcategory}.html',
        theme=MONOKAI
    )

    return df