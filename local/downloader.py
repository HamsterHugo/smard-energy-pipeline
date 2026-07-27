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

from config import FILTERS
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
