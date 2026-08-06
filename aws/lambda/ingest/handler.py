import logging
import datetime

import pandas as pd
import boto3

from smard_pipeline.config import CATEGORIES, COMBINED_CURRENT, S3_PREFIX_CURRENT
from smard_pipeline.config import S3_PREFIX_HISTORICAL
from smard_pipeline.logging_config import setup_lambda_logging
from smard_pipeline.ingest import download_and_process_current_week
from smard_pipeline.storage_s3 import save_df_to_s3, load_df_from_s3

def lambda_handler(event, context):
    # Initialize logger
    setup_lambda_logging()
    logger: logging.Logger = logging.getLogger(__name__)

    # Get bucket name
    ACCOUNT_ID: str = boto3.client('sts').get_caller_identity()['Account']
    BUCKET_NAME: str = f'smard-energy-pipeline-data-bucket-{ACCOUNT_ID}'

    # Dowload current week and preprocess the data
    df_tuple: tuple[pd.DataFrame, ...] = download_and_process_current_week()

    if df_tuple is None:
        logger.critical("Failed to download current week data. Aborting.")
        return

    # Push data to S3 /current
    id_list = [
        CATEGORIES[cat][subcat]['id']
        for cat in CATEGORIES
        for subcat in CATEGORIES[cat]
        if (CATEGORIES[cat][subcat]['daily_download']) and
        (not CATEGORIES[cat][subcat]['include_in_table'])
    ]
    file_list: list[str] = [COMBINED_CURRENT]
    file_list.extend([f"{id}_current.parquet" for id in id_list])
    zipped_data = list(zip(df_tuple, file_list))

    for df, file_name in zipped_data:
        save_df_to_s3(df, BUCKET_NAME, S3_PREFIX_CURRENT + file_name)

    # Check if it is monday. If yes check for completeness and archive data
    today = datetime.datetime.now().weekday()

    if today == 0:
        logger.info(
            "It is a monday. Check for completeness of last week's data."
        )

        for df, file_name in zipped_data:
            if len(df) == 672:
                logger.info(f"last week's data for {file_name} complete.")
                file_prefix: str = file_name.split('_')[0]
                logger.info("Loading historical data...")
                historical_df = load_df_from_s3(
                    BUCKET_NAME,
                    f"{S3_PREFIX_HISTORICAL}{file_prefix}_historical.parquet"
                )
                if historical_df is not None:
                    merged_df = pd.concat([historical_df, df], ignore_index=True)
                    success: bool = save_df_to_s3(
                        merged_df,
                        BUCKET_NAME,
                        f"{S3_PREFIX_HISTORICAL}{file_prefix}_historical.parquet"
                    )
                    if success:
                        logger.info(
                            f"Merged file {file_name} with historical data."
                        )
                    else:
                        logger.info(
                            f"Merge of file {file_name} with historical "
                            "data failed."
                        )
                else:
                    logger.error(
                        f"Failed to load historical data. Current data not "
                        "archived to historical data."
                    )