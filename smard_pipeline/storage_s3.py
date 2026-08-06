import logging
from io import BytesIO

import pandas as pd
import boto3

logger: logging.Logger = logging.getLogger(__name__)

def save_df_to_s3(df: pd.DataFrame, bucket: str, s3_key: str) -> bool:
    """Saves a DataFrame as Parquet to S3.

    Args:
        df (pd.DataFrame): DataFrame to save.
        bucket (str): S3 bucket name.
        s3_key (str): Target key in S3.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        buffer = BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)
        boto3.client('s3').put_object(
            Bucket=bucket,
            Key=s3_key,
            Body=buffer.getvalue()
        )
        logger.info(f"Saved DataFrame to s3://{bucket}/{s3_key}")
        return True
    except Exception as error:
        logger.error(f"Failed to save to s3://{bucket}/{s3_key}.", exc_info=error)
        return False

def load_df_from_s3(bucket: str, s3_key: str) -> pd.DataFrame | None:
    """Loads a Parquet file from S3 as DataFrame.

    Args:
        bucket (str): S3 bucket name.
        s3_key (str): Key in S3.

    Returns:
        pd.DataFrame | None: DataFrame or None if failed.
    """
    try:
        buffer = BytesIO()
        boto3.client('s3').download_fileobj(bucket, s3_key, buffer)
        buffer.seek(0)
        df: pd.DataFrame = pd.read_parquet(buffer)
        logger.info(f"Loaded DataFrame from s3://{bucket}/{s3_key}.")
        return df
    except Exception as error:
        logger.error(f"Failed to load from s3://{bucket}/{s3_key}.", exc_info=error)
        return None