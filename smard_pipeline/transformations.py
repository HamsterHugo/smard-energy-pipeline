import pandas as pd

def merge_raw_data(category: str, subcategory: str) -> pd.DataFrame:
    """Loads all raw_data for the queries category and subcategories and merges
    all timeseries into one data frame.

    Args:
        category (str): Top level category from FILTERS.
        subcategory (str): Subcategory key within the category

    Returns:
        pd.DataFrame: Contains all merged energy data from all week blocks.
            Columns are 'timestamp' and <subcategory>.
    """
    # TODO: Implement logic!
    pass