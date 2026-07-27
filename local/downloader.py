import sys
import time
from os import devnull
from pathlib import Path

import pandas as pd
from rich.traceback import install
from rich.progress import track
from rich.console import Console
from rich.terminal_theme import MONOKAI

# Add shared/ folder to Python path
sys.path.append(str(Path(__file__).parent.parent / "shared"))

from config import FILTERS, RAW_DATA_DIR, LOGS_DIR
from smard_api import is_current_week, get_timestamps, get_smard_timeseries

# Use install from rich for a better output of tracebacks
install()

# Define consols, one for the terminal and one for the logs.
console_terminal = Console()
console_log = Console(record=True, file=open(devnull, "w", encoding="utf-8"))

def update_raw_data(category: str, subcategory: str) -> None:
    """Downloads missing SMARD time series blocks for the given category.

    Args:
        category (str): Top-level category key from FILTERS
            (e.g. 'Stromerzeugung', 'Stromverbrauch').
        subcategory (str): Subcategory key within the category
            (e.g. 'Erdgas', 'Residuallast').
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

    # Set paths for downloads and logs.
    PATH_DICT: dict[str, str] = {
            'Stromerzeugung': 'power_generation',
            'Stromverbrauch': 'power_consumption',
            'Marktpreis': 'market_price',
            'Prognostizierte Erzeugung': 'forecasted_generation'
    }
    OUTPUT_DIR: Path = RAW_DATA_DIR / PATH_DICT[category]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Set message variable for log messages.
    msg: str = ''

    # Set filter_id for API call and emtpy list for failed downloads.
    filter_id: int = FILTERS[category][subcategory]
    failed_downloads: list[int] = []

    downloaded_timestamps: list[int] = [
        int(x.name.split('.')[0].split('_')[1])
        for x in OUTPUT_DIR.glob(f'*{filter_id}_*')
    ]
    if downloaded_timestamps and is_current_week(downloaded_timestamps[-1]):
        downloaded_timestamps.pop()
    
    online_timestamps: list[int] = get_timestamps(filter_id)

    if is_current_week(online_timestamps[-1]):
        online_timestamps.pop()

    if len(downloaded_timestamps) == len(online_timestamps):
        msg = f'[cyan][INFO][/] Historical files for {subcategory} ' \
        f'are up to date.'
        console_terminal.log(msg)
        console_log.log(msg)
    else:
        # Find number of missing files.
        number: int = len(online_timestamps)-len(downloaded_timestamps)
        if number == 1:
            msg = f'[cyan][INFO][/] There is {number} file missing ' \
                'for {subcategory}!'
            console_terminal.log(msg)
            console_log.log(msg)
        else:
            msg = f'[cyan][INFO][/] There are {number} files missing ' \
                f'for {subcategory}!'
            console_terminal.log(msg)
            console_log.log(msg)
        # Set counter variable for the missing files.
        counter = 0

        # Do the download with a progress bar.
        for timestamp in track(online_timestamps, description='[green] Processing...'):
            # Check if the data of the curret timestamp are missing. 
            if timestamp not in downloaded_timestamps:
                # The timestamp of the current timestamp is missing.
                # Start download. 
                # TODO: Implement the download 
                pass

        if counter < number:
            # TODO Implement log messages for updating the progress.
            pass
        else:
            pass

    # Save the logs.
    console_log.save_html(
        LOGS_DIR/f'log_{category}_{subcategory}.html',
        theme=MONOKAI
    )