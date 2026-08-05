import logging

import pandas as pd

from smard_pipeline.config import CATEGORIES
from smard_pipeline.smard_api import get_timestamps, get_smard_timeseries
from smard_pipeline.smard_api import is_current_week

logger: logging.Logger = logging.getLogger(__name__)

def fetch_current_week(category: str, subcategory: str) -> pd.DataFrame | None:
    """Fetches the current week's time series for the given category.

    Args:
        category (str): Top_level category key from CATEGORIES.
        subcategory (str): Subcategory key within the category.

    Returns:
        pd.DataFrame | None: The DataFrame with current week's data, or None if
        no current data is available.
    """
    # Check for valid arguments.
    if category not in CATEGORIES:
        logger.error(f"Unkown category: '{category}'")
        logger.error(f"Available categories are: '{list(CATEGORIES.keys())}'")
        return None

    if subcategory not in CATEGORIES[category]:
        logger.error(f"Unkown subcategory: '{subcategory}'")
        logger.error(
            f"Available subcategories: '{list(CATEGORIES[category].keys())}'"
        )
        return None

    smard_id: int = CATEGORIES[category][subcategory]['id']
    timestamp: int = get_timestamps(smard_id)[-1]

    if not is_current_week(timestamp):
        logger.warning(
            f"No current data for {category}: {subcategory} available."
        )
        return None

    logger.info(
        f"Fetching data of current week for {category}: {subcategory}..."
    )

    try:
        data: dict = get_smard_timeseries(smard_id, timestamp)
        df: pd.DataFrame = pd.DataFrame(
            data['series'],
            columns=['timestamps', 'value_mwh']
        )
        df = df.dropna()
        logger.info(f"Fetched {len(df)} rows.", extra={"status": "success"})
        return df
    except Exception as error:
        logger.critical(
            f"Failed to fetch {category}: {subcategory}.",
            exc_info=error
        )
        return None