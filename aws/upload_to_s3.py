import logging
import re
import subprocess
import json
from pathlib import Path

import boto3

from smard_pipeline.config import PREPROCESSED_DATA_DIR, COMBINED_HISTORICAL
from smard_pipeline.config import MARKET_PRICE_HISTORICAL, NUCLEAR_HISTORICAL
from smard_pipeline.logging_config import setup_logging, save_log_to_html

ACCOUNT_ID: str = boto3.client('sts').get_caller_identity()['Account']
BUCKET_NAME: str = f'smard-energy-pipeline-data-bucket-{ACCOUNT_ID}'
FRONTEND_DIR: Path = Path(__file__).parent.parent / 'dashboard' / 'frontend'

def upload_file(local_path: Path, s3_key: str, ConentType: str = None) -> bool:
    """Uploads a single file to S3.

    Args:
        local_path (Path): Local path to the file.
        s3_key (str): Target key in S3.
        ConentType (str, optional): The ContentType needed for the browser.
            Defaults to None.

    Returns:
        bool: _description_
    """
    if not local_path.exists():
        logger.warning(f"File not found: {local_path.name}. Skipping...")
        return False
    try:
        if ConentType is not None:
            s3.upload_file(
                str(local_path),
                BUCKET_NAME,
                s3_key,
                ExtraArgs={'ContentType': ConentType}
            )
        else:
            s3.upload_file(str(local_path), BUCKET_NAME, s3_key)
        logger.info(
            f'{local_path.name} -> s3://{BUCKET_NAME}/{s3_key}',
            extra={"status": "success"}
        )
        return True
    except Exception as error:
        logger.error(f"Failed to upload {local_path.name}: {error}")
        return False

def upload_historical_data() -> None:
    """Uploads all historical parquet files to S3."""
    logger.info('Uploading historical data...')
    counter: int = 0
    files_dir: list = [
        COMBINED_HISTORICAL,
        NUCLEAR_HISTORICAL,
        MARKET_PRICE_HISTORICAL
    ]
    l: int = len(files_dir)
    for file in files_dir:
        success = upload_file(PREPROCESSED_DATA_DIR / file, f'historical/{file}')
        if success: counter += 1

    if counter < l:
        logger.info(f"Upload: {counter}/{l} files", extra={"status": "report"})
    else:
        logger.info(f"Upload: {counter}/{l} files", extra={"status": "complete"})

def upload_frontend() -> None:
    logger.info(f"Uploading frontend files...")
    frontend_files = [
        ("index.html", 'text/html'),
        ("style.css", 'text/css'),
        ("script.js", 'application/javascript'),
        ("favicon.ico", 'image/x-icon')
    ]
    l: int = len(frontend_files)
    counter: int = 0
    for file, ContentType in frontend_files:
        success = upload_file(FRONTEND_DIR / file, file, ConentType=ContentType)
        if success: counter += 1

    if counter < l:
        logger.info(f"Upload: {counter}/{l} files", extra={"status": "report"})
    else:
        logger.info(f"Upload: {counter}/{l} files", extra={"status": "complete"})

if __name__ == '__main__':
    # Initialze logger.
    setup_logging(level=logging.INFO)
    logger: logging.Logger = logging.getLogger('upload_to_s3')

    # Get the API url from terraform output.
    logger.info('Get the API URL from the terraform output...')
    result = subprocess.run(
        ['terraform', 'output', '-json'],
        cwd='../terraform',
        capture_output=True,
        text=True
    )

    try:
        outputs: dict = json.loads(result.stdout)
        api_url: str = outputs['api_url']['value']
        website_url: str = outputs['website_url']['value']
        logger.info(f"API URL found: {api_url}", extra={"status": "success"})
    except Exception:
        logger.critical(
            f"Error while parsing the terraform output!",
            exc_info=True
        )
        exit(1)

    # Write API URL into script.js.
    script_js: Path = FRONTEND_DIR / 'script.js'
    content: str = script_js.read_text()

    old_url_pattern = r'https:.+prod'
    content = re.sub(old_url_pattern, api_url, content)
    script_js.write_text(content)
    logger.info("Replaced api_url in 'script.js'.", extra={"status": "success"})

    # Upload all needed data to the s3 bucket.
    s3 = boto3.client('s3')
    upload_historical_data()
    upload_frontend()

    logger.info(f"Dashboard-URL: {website_url}")

    save_log_to_html("upload_report")