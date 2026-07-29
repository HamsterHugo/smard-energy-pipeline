import boto3

s3 = boto3.client('s3')

account_id: str = boto3.client('sts').get_caller_identity()['Account']
BUCKET_NAME: str = f'smard-energy-pipeline-data-{account_id}'