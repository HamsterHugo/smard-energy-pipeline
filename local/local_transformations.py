import logging
from pathlib import Path

import pandas as pd

from smard_pipeline.config import CATEGORIES, RAW_DATA_DIR, PREPROCESSED_DATA_DIR
from smard_pipeline.transformations import convert_timestamp_column
from smard_pipeline.transformations import get_current_timestamp

logger = logging.getLogger(__name__)

def process_and_store_single_timeseries(category: str, subcategory: str) -> None:
    """Processes and stores a single time series from the directory
    'current_week' to the folder 'preprocessed_data'. This function shall be
    used only for these time series that are not contained in the big table.


    Args:
        category (str): Name of the category.
        subcategory (str): Name of the subcategory.
    """
    # Settings
    smard_id: int = CATEGORIES[category][subcategory]['id']
    current_timestamp: int = get_current_timestamp()
    file_name: str = f"{smard_id}_{current_timestamp}.parquet"
    file: Path = RAW_DATA_DIR / "current_week" / file_name

    # Check, if the file exists. If not, end the function. 
    if not file.exists():
        logger.warning(f"File {file} not found. You have to download it.")
        return
    else:
        logger.info(f"File {file_name} found.")

    # Load the file.
    try:
        df: pd.DataFrame = pd.read_parquet(file)
        df.columns = ('timestamps', subcategory)
        df['timestamps'] = convert_timestamp_column(df['timestamps'])
        logger.info("File loaded and processed successfully.")

        output_dir: Path = PREPROCESSED_DATA_DIR / f"{smard_id}_current.parquet"

        df.to_parquet(output_dir)
        logger.info(f'File saved: {output_dir.name}', extra={"status": "success"})
    except Exception as e:
        logger.error(
            f"Not able to load or process the file {file_name}.",
            exc_info=e
        )