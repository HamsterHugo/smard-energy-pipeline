from os import devnull
from pathlib import Path

import pandas as pd
from rich.traceback import install
from rich.console import Console
from rich.terminal_theme import MONOKAI

from smard_pipeline.config import RAW_DATA_DIR, PREPROCESSED_DATA_DIR, LOGS_DIR
from smard_pipeline.config import PATH_DICT, CATEGORIES

# Use install from rich for a better output of tracebacks
install()

# Define consols, one for the terminal and one for the logs.
console = Console(record=True)

def convert_timestamp_column(
        series: pd.Series,
        timezone: str = 'Europe/Berlin'
    ) -> pd.Series:
    """Converts a Series of Unix timestamps in milliseconds to
    timezone-aware datetimes.

    Args:
        series (pd.Series): Series with Unix timestamps in milliseconds.
        timezone (str): Target timezone. Defaults to 'Europe/Berlin'.

    Returns:
        pd.Series: Series with timezone-aware datetime objects.
    """
    return pd.to_datetime(series, unit='ms', utc=True).dt.tz_convert(timezone)

def merge_raw_data(category: str, subcategory: str) -> None:
    """Reads all raw weekly parquet files for the given category and
    subcategory, merges them into a single time series and saves the
    result as a parquet file.

    Args:
        category (str): Top level category from FILTERS.
        subcategory (str): Subcategory key within the category
    """
    # Check for valid arguments.
    if category not in CATEGORIES:
        console.log(
            f"[bold bright_red][ERROR][/] Unknown category: '{category}'"
        )
        console.log(
            f"[cyan][INFO][/] Available categories: {list(CATEGORIES.keys())}"
        )
        return
    
    if subcategory not in CATEGORIES[category]:
        console.log(
            f"[bold bright_red][ERROR][/] Unknown subcategory: '{subcategory}'"
        )
        console.log(
            f"[cyan][INFO][/] Available subcategories: "
            f"{list(CATEGORIES[category].keys())}"
        )
        return

    input_dir: Path = RAW_DATA_DIR / PATH_DICT[category]
    PREPROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    smard_id: int = CATEGORIES[category][subcategory]['id']

    weekly_blocks: list[pd.DataFrame] = [
        pd.read_parquet(file)
        for file in sorted(input_dir.glob(f'{smard_id}_*.parquet'))
    ]

    if not weekly_blocks:
        console.log(f"[yellow][WARNING][/] No files found for {subcategory}.")
        console.log(
            f"[yellow][WARNING][/] You have to download "
            f"the data for {subcategory}."
        )
    else:
        df: pd.DataFrame = pd.concat(weekly_blocks, ignore_index=True)
        df.columns = ['timestamps', subcategory]
        df = df.dropna()
        if CATEGORIES[category][subcategory]['convert_timestamps']:
            df['timestamps'] = convert_timestamp_column(df['timestamps'])
        console.log(f"[bold green][SUCCESS][/] Raw data for {subcategory} merged!")
        output_path = PREPROCESSED_DATA_DIR / f'{smard_id}_historical.parquet'
        df.to_parquet(output_path)
        console.log(f"[bold green][SUCCESS][/] File saved {output_path}.")

    console.save_html(
        LOGS_DIR/f'merge_log_{category}_{subcategory}.html',
        theme=MONOKAI
    )

def merge_all_categories() -> None:
    """Merges all preprocessed parquet files for active energy categories,
    consumption and market price into a single combined parquet file.
    """
    df_list: list[pd.DataFrame] = []

    for category, subcategory in CATEGORIES.items():
        for name, config in subcategory.items():
            if config['convert_timestamps']:
                continue

            smard_id: int = config['id']
            file: Path = PREPROCESSED_DATA_DIR / f'{smard_id}_historical.parquet'

            if not file.exists():
                console.log(
                    f"[yellow][WARNING][/] File not found for {category}: "
                    f"{name}, skipping..."
                )
                continue

            df: pd.DataFrame = pd.read_parquet(file)
            df_list.append(df)
            console.log(f"[bold green][SUCCESS][/] Loaded {category}: {name}.")

    if not df_list:
        console.log(
            f"[bold bright_red][ERROR][/] No preprocessed files found."
        )
    else:
        combined_df: pd.DataFrame = df_list[0]
        for df in df_list[1:]:
            combined_df = pd.merge(combined_df, df, how='inner', on='timestamps')

        combined_df['timestamps'] = convert_timestamp_column(combined_df['timestamps'])
        output_path = PREPROCESSED_DATA_DIR / 'combined_historical.parquet'
        combined_df.to_parquet(output_path)
        console.log(
            f"[bold green][SUCCESS][/] Combined file saved: {output_path}."
        )

    console.save_html(
        LOGS_DIR/f'combined_log.html',
        theme=MONOKAI
    )