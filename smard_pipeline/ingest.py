import logging

import pandas as pd

from smard_pipeline.current_week import fetch_current_week
from smard_pipeline.transformations import convert_timestamp_column
from smard_pipeline.config import CATEGORIES

logger: logging.Logger = logging.getLogger(__name__)

def download_and_process_current_week() -> tuple[pd.DataFrame, ...] | None:
    """Downloads and processes the current week's data for all relevant
        categories.

    Returns:
        tuple[pd.DataFrame] | None: A tuple with data frame. The first one 
            contains the most data in one table. The remaining ones are the
            categories which don't belong to the big table. None if one or more
            required data are missing.
    """
    # Collect all categories for the daily download.
    category_types: list = [
        (cat, subcat) for cat in CATEGORIES
        for subcat in CATEGORIES[cat]
        if CATEGORIES[cat][subcat]['daily_download']
    ]

    # Fetch all the categories for the daily download and adapt their columns.
    fetched_data = {}
    for cat, subcat in category_types:
        result = fetch_current_week(cat, subcat)
        if result is None or len(result) == 0:
            logger.critical(
                f'Data for {cat}: {subcat} is missing. '
                f'No merged data frame created!'
            )
            return None
        df = result[0]
        df.columns = ['timestamps', subcat]
        fetched_data[(cat, subcat)] = {
            'data': df,
            'include_in_table': CATEGORIES[cat][subcat]['include_in_table']
        }

    # Filter for all categories which shall be in the big data table.
    df_table_list: list[pd.DataFrame] = [
        fetched_data[(cat,subcat)]['data']
        for cat, subcat in category_types 
        if fetched_data[(cat,subcat)]['include_in_table']
    ]

    # Filter for all other categories which shall be stored in a single file.
    df_single_data_list: list[pd.DataFrame] = [
        fetched_data[(cat,subcat)]['data']
        for cat, subcat in category_types 
        if not fetched_data[(cat,subcat)]['include_in_table']
    ]

    # Merge the data frames to one data frame.
    combined_df: pd.DataFrame = df_table_list[0]
    for df in df_table_list[1:]:
        combined_df = pd.merge(combined_df, df, how='inner', on='timestamps')

    # Convert the timestamps from integers to human readable datetimes.
    combined_df['timestamps'] = convert_timestamp_column(
        combined_df['timestamps']
    )
    for df in df_single_data_list:
        df['timestamps'] = convert_timestamp_column(df['timestamps'])

    # Put all data frames together in one tuple.
    result = [combined_df]
    result.extend(df_single_data_list)
    result = tuple(result)

    return result
