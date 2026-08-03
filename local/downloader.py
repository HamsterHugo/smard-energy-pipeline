import time
import logging
from pathlib import Path

import pandas as pd

from smard_pipeline.config import CATEGORIES, RAW_DATA_DIR, PATH_DICT
from smard_pipeline.smard_api import is_current_week, get_timestamps, get_smard_timeseries

logger = logging.getLogger(__name__)

def update_raw_data(category: str, subcategory: str) -> None:
    """Downloads missing SMARD time series blocks for the given category.

    Args:
        category (str): Top-level category key from CATEGORIES
            (e.g. 'Stromerzeugung', 'Stromverbrauch').
        subcategory (str): Subcategory key within the category
            (e.g. 'Erdgas', 'Residuallast').
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

    # Set paths for downloads and logs.
    OUTPUT_DIR: Path = RAW_DATA_DIR / PATH_DICT[category]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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
        logger.info(f"Historical files for {category}: {subcategory} are up to date.")
    else:
        # Find number of missing files.
        number: int = len(online_timestamps)-len(downloaded_timestamps)
        if number == 1:
            logger.info(f"There is {number} file missing for {category}: {subcategory}.")
        else:
            logger.info(f"There are {number} files missing for {category}: {subcategory}.")
        # Set counter variable for the missing files.
        counter = 0

        # Do the download with a progress bar.
        for timestamp in online_timestamps:
            # Check if the data of the curret timestamp are missing. 
            if timestamp not in downloaded_timestamps:
                # The timestamp of the current timestamp is missing.
                # Start the download. 
                file_name = f'{smard_id}_{timestamp}.parquet'
                logger.info(f"Missing file detected: {file_name}")

                try:
                    data = get_smard_timeseries(smard_id, timestamp)
                    df = pd.DataFrame(
                        data['series'],
                        columns=['timestamp', 'value_mwh']
                    )
                    output_path = OUTPUT_DIR / file_name
                    df.to_parquet(output_path, index=False)
                    counter += 1
                    logger.info(f"File {file_name} saved.", extra={"status": "success"})
                    if counter < number:
                        logger.info(f"Update: {counter}/{number}")
                    else:
                        logger.info(f"Update: {counter}/{number}")
                except Exception as error:
                    failed_downloads.append(timestamp)
                    logger.error(f"Download for {category}: {subcategory} at timestamp {timestamp} failed!", exc_info=error)
                # Small time out for API request.
                time.sleep(0.2)

        if counter < number:
            logger.info(f"Update was not successfull. There are {number-counter} files missing!", extra={"status": "fail"})
            logger.info("Missing timestamps are:")
            for item in failed_downloads:
                logger.info(f"    {item}")
        else:
            logger.info(f"Historical files for {category}: {subcategory} are now up to date!", extra={"status": "complete"})

def download_current_week(category: str, subcategory: str) -> None:
    """Downloads the time series block of the current week for the queried
    category and subcategory.

    Args:
        category (str): Top-level category key from CATEGORIES
            (e.g. 'Stromerzeugung', 'Stromverbrauch').
        subcategory (str): Subcategory key within the category
            (e.g. 'Erdgas', 'Residuallast').
    """
    # Check for valid arguments.
    if category not in CATEGORIES:
        logger.error(f"Unkown category: '{category}'")
        logger.error(f"Available categories: '{list(CATEGORIES.keys())}'")
        return
    
    if subcategory not in CATEGORIES[category]:
        logger.error(f"Unkown subcategory: '{subcategory}'")
        logger.error(f"Available subcategories: '{list(CATEGORIES[category].keys())}'")
        return

    # Set paths for downloads and logs.
    OUTPUT_DIR: Path = RAW_DATA_DIR / 'current_week'
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Setting smard_id for API request.
    smard_id: int = CATEGORIES[category][subcategory]['id']

    timestamp: int = get_timestamps(smard_id)[-1]

    if not is_current_week(timestamp):
        logger.warning(f"There are nor current data for {category}: {subcategory}")
    else:
        logger.info(f'Current data available for {category}: {subcategory}.')
        logger.info('Start downloading...')

        file_name: str = f'{smard_id}_{timestamp}.parquet'
        try:
            data = get_smard_timeseries(smard_id, timestamp)
            df = pd.DataFrame(
                data['series'],
                columns=['timestamp', 'value_mwh']
            )
            output_path = OUTPUT_DIR / file_name
            df.to_parquet(output_path, index=False)
            logger.info(f'Saved file: {file_name}.', extra={"status": "success"})
        except Exception as error:
            logger.critical(error, exc_info=error)