import boto3
from rich.console import Console
from rich.traceback import install

from smard_pipeline.config import PREPROCESSED_DATA_DIR, COMBINED_HISTORICAL
from smard_pipeline.config import MARKET_PRICE_HISTORICAL, NUCLEAR_HISTORICAL

install()

console: Console = Console()

account_id: str = boto3.client('sts').get_caller_identity()['Account']
BUCKET_NAME: str = f'smard-energy-pipeline-data-bucket-{account_id}'
S3_PREFIX: str = 'historical/'

s3 = boto3.client('s3')

for file in [COMBINED_HISTORICAL, NUCLEAR_HISTORICAL, MARKET_PRICE_HISTORICAL]:
    local_path = PREPROCESSED_DATA_DIR / file
    if not local_path.exists():
        console.log(f'[bold yellow]WARNING[/] File not found: {file}. Skipping...')
        continue
    
    s3_key = S3_PREFIX + file
    try:
        s3.upload_file(str(local_path), BUCKET_NAME, s3_key)
        console.log(f'[bold green]SUCCESS[/] Uploaded file {file} -> s3://{BUCKET_NAME}/{s3_key}')
    except Exception as e:
        console.log(f'[bold bright_red]ERROR[/] Failed to upload file {file}: {e}')