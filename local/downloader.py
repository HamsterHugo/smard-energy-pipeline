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