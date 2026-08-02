import logging
from pathlib import Path

import pandas as pd

from smard_pipeline.config import RAW_DATA_DIR, PREPROCESSED_DATA_DIR, LOGS_DIR
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
        logger.info(f"File saved {output_path}.", extra={"status": "success"})

def merge_all_categories() -> None:
    """Merges all preprocessed parquet files for active energy categories,
    consumption and market price into a single combined parquet file.
    """
    df_list: list[pd.DataFrame] = []

    for category, subcategory in CATEGORIES.items():
        for name, config in subcategory.items():
            if not config['include_in_table']:
                continue

            smard_id: int = config['id']
            file: Path = PREPROCESSED_DATA_DIR / f'{smard_id}_historical.parquet'

            if not file.exists():
                logger.warning(
                    f"File not found for {category}: {name}, skipping..."
                )
                continue

            df: pd.DataFrame = pd.read_parquet(file)
            df_list.append(df)
            logger.info(f"Loaded {category}: {name}.", extra={"status": "success"})

    if not df_list:
        logger.error("No preprocessed files found.")
    else:
        combined_df: pd.DataFrame = df_list[0]
        for df in df_list[1:]:
            combined_df = pd.merge(combined_df, df, how='inner', on='timestamps')

        combined_df['timestamps'] = convert_timestamp_column(combined_df['timestamps'])
        output_path = PREPROCESSED_DATA_DIR / 'combined_historical.parquet'
        combined_df.to_parquet(output_path)
        logger.info(f"Combined file saved: {output_path}.", extra={"status": "success"})
