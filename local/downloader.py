import time
from os import devnull
from pathlib import Path

import pandas as pd
from rich.traceback import install
from rich.progress import track
from rich.console import Console
from rich.terminal_theme import MONOKAI

from smard_pipeline.config import CATEGORIES, RAW_DATA_DIR, LOGS_DIR, PATH_DICT
from smard_pipeline.smard_api import is_current_week, get_timestamps, get_smard_timeseries

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
    if category not in CATEGORIES:
        console_terminal.log(
            f"[bold bright_red][ERROR][/] Unknown category: '{category}'"
        )
        console_terminal.log(
            f"[cyan][INFO][/] Available categories: {list(CATEGORIES.keys())}"
        )
        return
    
    if subcategory not in CATEGORIES[category]:
        console_terminal.log(
            f"[bold bright_red][ERROR][/] Unknown subcategory: '{subcategory}'"
        )
        console_terminal.log(
            f"[cyan][INFO][/] Available subcategories: "
            f"{list(CATEGORIES[category].keys())}"
        )
        return

    # Set paths for downloads and logs.
    OUTPUT_DIR: Path = RAW_DATA_DIR / PATH_DICT[category]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Set message variable for log messages.
    msg: str = ''

    # Set smard_id for API call and emtpy list for failed downloads.
    smard_id: int = CATEGORIES[category][subcategory]['id']
    failed_downloads: list[int] = []

    downloaded_timestamps: list[int] = [
        int(x.name.split('.')[0].split('_')[1])
        for x in OUTPUT_DIR.glob(f'{smard_id}_*')
    ]
    if downloaded_timestamps and is_current_week(downloaded_timestamps[-1]):
        downloaded_timestamps.pop()
    
    online_timestamps: list[int] = get_timestamps(smard_id)

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
                f'for {subcategory}!'
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
                # Start the download. 
                file_name = f'{smard_id}_{timestamp}.parquet'
                msg = f'[cyan][INFO][/] Missing file detected: {file_name}'
                console_log.log(msg)

                try:
                    data = get_smard_timeseries(smard_id, timestamp)
                    df = pd.DataFrame(
                        data['series'],
                        columns=['timestamp', 'value_mwh']
                    )
                    output_path = OUTPUT_DIR / file_name
                    df.to_parquet(output_path, index=False)
                    counter += 1
                    msg = f'[bold green][SUCCESS][/] {file_name} saved ' \
                        f'successfully! [bold green]✓[/]'
                    console_log.log(msg)
                    if counter < number:
                        msg = f'[cyan][INFO][/] {counter}/{number} updated!'
                        console_log.log(msg)
                    else:
                        msg = f'[bold green][COMPLETED][/] ' \
                            f'{counter}/{number} updated!'
                        console_log.log(msg)
                except Exception as Error:
                    failed_downloads.append(timestamp)
                    console_log.print_exception()
                    msg = f'[bold bright_red][FAILURE][/] Download for Energy ' \
                        f'data for timestamp {timestamp} for {subcategory} ' \
                        f'failed! [bold bright_red]✗[/]'
                    console_log.log()
                    msg = f'[bold bright_red]ERROR:[/] {Error}'
                    console_log.log(msg)
                # Small time out for API request.
                time.sleep(0.2)

        if counter < number:
            msg = f'[bold red]WARNING[/] Update was not successfull. There ' \
                f'are {number-counter} files missing! [bold bright_red]✗[/]'
            console_terminal.log(msg)
            console_log.log(msg)
            msg = '[bold bright_red]✗[/]   Missing timestamps are:'
            console_terminal.log(msg)
            console_log.log(msg)
            for item in failed_downloads:
                msg = f'  {item}'
                console_terminal.log(msg)
                console_log.log(msg)
        else:
            msg = f'[bold green]UPDATE COMPLETED![/] Historical files for ' \
                f'{subcategory} are up to date. [bold green]✓[/]'
            console_terminal.log(msg)
            console_log.log(msg)

    # Save the logs.
    console_log.save_html(
        LOGS_DIR/f'log_{category}_{subcategory}.html',
        theme=MONOKAI
    )