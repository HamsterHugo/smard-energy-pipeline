import logging
import datetime
from pathlib import Path

import pandas as pd

from smard_pipeline.config import RAW_DATA_DIR, PREPROCESSED_DATA_DIR
from smard_pipeline.config import PATH_DICT, CATEGORIES

logger = logging.getLogger(__name__)

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
        logger.error(f"Unkown category: '{category}'")
        logger.info(f"Available categories: {list(CATEGORIES.keys())}")
        return
    
    if subcategory not in CATEGORIES[category]:
        logger.error(f"Unkown subcategory: '{subcategory}'")
        logger.error(f"Available subcategories: '{list(CATEGORIES[category].keys())}'")
        return

    logger.info(f"Search data for {category}: {subcategory}...")
    input_dir: Path = RAW_DATA_DIR / PATH_DICT[category]
    PREPROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    smard_id: int = CATEGORIES[category][subcategory]['id']

    weekly_blocks: list[pd.DataFrame] = [
        pd.read_parquet(file)
        for file in sorted(input_dir.glob(f'{smard_id}_*.parquet'))
    ]

    if not weekly_blocks:
        logger.error(f"No files found for {category}: {subcategory}.")
        logger.warning(f"You have to download the data for {category}: {subcategory}")
    else:
        logger.info(f"Found data for {len(weekly_blocks)} weeks.")
        logger.info(f"Start merging...")
        df: pd.DataFrame = pd.concat(weekly_blocks, ignore_index=True)
        df.columns = ['timestamps', subcategory]
        df = df.dropna()
        if not CATEGORIES[category][subcategory]['include_in_table']:
            df['timestamps'] = convert_timestamp_column(df['timestamps'])
        logger.info(f"Raw data for {category}: {subcategory} merged!", extra={"status": "success"})
        output_path = PREPROCESSED_DATA_DIR / f'{smard_id}_historical.parquet'
        df.to_parquet(output_path)
        logger.info(f"File saved: {output_path.name}.", extra={"status": "success"})

def get_current_timestamp() -> int:
    """Computes the timestamp of the last monday at 00:00 AM for the smard API.

    Returns:
        int: The timestamp of the current week.
    """
    now = datetime.datetime.now()
    days_since_monday = now.weekday()
    last_monday = now - datetime.timedelta(days=days_since_monday)
    last_monday = last_monday.replace(hour=0, minute=0, second=0, microsecond=0)

    return int(last_monday.timestamp()*1000)

def combine_data(data_type: str) -> None:
    """Takes all historical or current timeseries and combines it into one data
    frame and saves it as a parquet file.

    NOTICE: All needed files have to be there. For the historical data you have
    to merge alls week blocks to one time series. After that you can apply this
    function for merging. For the data of the current week you have to download
    them first.

    Args:
        data_type (str): Has to be either 'current' or 'historical'.
    """
    df_list: list = []
    missing_files: list = []
    counter: int = 0
    if data_type == 'current':
        current_timestamp = get_current_timestamp()

    for category, subcategory in CATEGORIES.items():
        for name, config in subcategory.items():
            if not config['include_in_table']:
                continue

            smard_id: int = config['id']
            if data_type == 'historical':
                file: Path = PREPROCESSED_DATA_DIR / f'{smard_id}_historical.parquet'
            else:
                file: Path = RAW_DATA_DIR / "current_week" / f"{smard_id}_{current_timestamp}.parquet"
            counter += 1

            if not file.exists():
                logger.warning(
                    f"File {file.name} not found. You have to "
                    f"{'merge' if data_type == 'historical' else 'download'} "
                    f"the {data_type} data for {category}: {name}.")
                missing_files.append((category, name))
                continue

            df: pd.DataFrame = pd.read_parquet(file)
            if data_type == 'current': df.columns = ('timestamps', name)
            df_list.append(df)
            logger.info(f'File found for {category}: {name} - {file.name}', extra={"status": "success"})

    if not df_list:
        logger.error(f"No data found. You have to {'merge' if data_type == 'historical' else 'download'} it.")
    elif (l:=len(df_list)) < counter:
        logger.error(f"There are {counter-l} files missing, namely:")
        for category, subcategory in missing_files:
            logger.error(f"    {category}: {subcategory}")
    else:
        combined_df: pd.DataFrame = df_list[0]
        for df in df_list[1:]:
            combined_df = pd.merge(combined_df, df, how='inner', on='timestamps')

        combined_df['timestamps'] = convert_timestamp_column(combined_df['timestamps'])
        output_path = PREPROCESSED_DATA_DIR / f'combined_{data_type}.parquet'
        combined_df.to_parquet(output_path)
        logger.info(f"Combined file saved: {output_path.name}.", extra={"status": "complete"})