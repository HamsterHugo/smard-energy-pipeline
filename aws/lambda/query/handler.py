import logging
import json

import pandas as pd
import boto3

from smard_pipeline.logging_config import setup_lambda_logging
from smard_pipeline.storage_s3 import load_df_from_s3
from smard_pipeline.config import COMBINED_HISTORICAL, COMBINED_CURRENT
from smard_pipeline.config import S3_PREFIX_CURRENT, S3_PREFIX_HISTORICAL
from smard_pipeline.config import MARKET_PRICE_HISTORICAL, MARKET_PRICE_CURRENT
from smard_pipeline.config import NUCLEAR_HISTORICAL

def lambda_handler(event, context):
    # Initialize logger
    setup_lambda_logging()
    logger: logging.Logger = logging.getLogger(__name__)

    # Read parameter from event
    params: dict = event.get('queryStringParameters', {}) or {}
    endpoint: str = params.get('endpoint', 'data')
    date_from: str = params.get('from', '2026-07-01')
    date_to: str = params.get('to', '2026-07-31')

    # Bucket name
    ACCOUNT_ID: str = boto3.client('sts').get_caller_identity()['Account']
    BUCKET_NAME: str = f'smard-energy-pipeline-data-bucket-{ACCOUNT_ID}'

    # Load data according endpoint
    if endpoint == 'data':
        historical_file: str = S3_PREFIX_HISTORICAL + COMBINED_HISTORICAL
        current_file: str = S3_PREFIX_CURRENT + COMBINED_CURRENT
    elif endpoint == 'price':
        historical_file: str = S3_PREFIX_HISTORICAL + MARKET_PRICE_HISTORICAL
        current_file: str = S3_PREFIX_CURRENT + MARKET_PRICE_CURRENT
    elif endpoint == 'nuclear':
        historical_file: str = S3_PREFIX_HISTORICAL + NUCLEAR_HISTORICAL
        current_file = None
    else:
        logger.error(f'Unkown endpoint: {endpoint}')
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow_origin': '*'},
            'body': json.dumps({'error': f"Unkown endpoint: {endpoint}"})
        }

    # Load historical data
    df: pd.DataFrame = load_df_from_s3(BUCKET_NAME, historical_file)
    if df is None:
        logger.error(f"Failed to load historical data: {historical_file}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Failed to load historical data'})
        }

    # Load current data
    if current_file is not None:
        current_df: pd.DataFrame = load_df_from_s3(BUCKET_NAME, current_file)
        if current_file is not None:
            df = pd.concat([df, current_df], ignore_index=True)
        else:
            logger.warning(f"Current data not available: {current_file}")

    # Filter for timestamps
    df['timestamps'] = pd.to_datetime(df['timestamps'], utc=True)
    data_from_dt = pd.to_datetime(date_from, utc=True)
    date_to_dt = pd.to_datetime(date_to, utc=True)
    df = df[
        (df['timestamps'] >= data_from_dt) &
        (df['timestamps'] <= date_to_dt)
    ]

    logger.info(f"Returning {len(df)} rows.")
    
    # Return JSON
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(df.to_dict(orient='records'), default=str)
    }