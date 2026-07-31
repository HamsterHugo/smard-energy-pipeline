import sys

from smard_pipeline.config import CATEGORIES
from downloader import download_current_week

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python 03_download_current.py <category> <subcategory>")
        print("    Example: python 03_download_current.py Stromerzeugung Erdgas")
        print("    Example: python 03_download_current.py Stromverbrauch Residuallast")
        print('For looping through all subcategories use:')
        print('    python 03_download_current.py <category> all')
        sys.exit(1)

    category = sys.argv[1]
    subcategory = sys.argv[2]

    if subcategory == 'all':
        for current_subcategory in CATEGORIES[category]:
            download_current_week(category, current_subcategory)
    else:
        download_current_week(category, subcategory)