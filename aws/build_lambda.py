import shutil
import subprocess
import zipfile
import logging
from pathlib import Path

from smard_pipeline.logging_config import setup_logging, save_log_to_html

ROOT_DIR = Path(__file__).parent.parent
LAYER_DIR = ROOT_DIR / 'layer' / 'python'
SMARD_PIPELINE_DIR = ROOT_DIR / 'smard_pipeline'
LAYER_ZIP = Path(__file__).parent / 'layer.zip'

setup_logging()

logger: logging.Logger = logging.getLogger()


def build_layer() -> None:
    """Builds the Lambda Layer ZIP file containing all Python dependencies
    and the smard_pipeline package. Cleans up the layer directory afterwards.
    """
    logger.info("Building Lambda Layer...")

    # Clean up old layer content
    if LAYER_DIR.exists():
        shutil.rmtree(LAYER_DIR)
    LAYER_DIR.mkdir(parents=True)

    # Copy smard_pipeline package
    shutil.copytree(SMARD_PIPELINE_DIR, LAYER_DIR / 'smard_pipeline')
    logger.info("smard_pipeline copied", extra={"status": "success"})

    # Install dependencies
    logger.info("Installing dependencies...")
    subprocess.run([
        'pip', 'install',
        'pandas', 'boto3', 'pyarrow', 'requests',
        '-t', str(LAYER_DIR),
        '--quiet'
    ], check=True)
    logger.info("Dependencies installed", extra={"status": "success"})

    # Create ZIP
    logger.info("Creating ZIP...")
    with zipfile.ZipFile(LAYER_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in LAYER_DIR.rglob('*'):
            if file.is_file():
                zf.write(file, file.relative_to(ROOT_DIR / 'layer'))

    zip_size = LAYER_ZIP.stat().st_size / 1_000_000
    logger.info(f"ZIP created: {zip_size:.1f} MB", extra={"status": "success"})

    # Clean up layer directory
    shutil.rmtree(ROOT_DIR / 'layer')
    logger.info("Layer directory cleaned up", extra={"status": "success"})

    logger.info("Done!",extra={"status": "complete"})


if __name__ == '__main__':
    build_layer()
    save_log_to_html("lambda_log.html")