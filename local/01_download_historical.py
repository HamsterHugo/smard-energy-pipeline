import sys
from pathlib import Path

# Add shared/ folder to Python path
sys.path.append(str(Path(__file__).parent.parent / "shared"))

from config import FILTERS
from downloader import update_raw_data

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python 01_download_historical.py <category> <subcategory>")
        print("Example: python 01_download_historical.py Stromerzeugung Erdgas")
        print("Example: python 01_download_historical.py Stromverbrauch Residuallast")
        print('For looping through all subcategories use:')
        print('python 01_download_historical.py <category> all')
        sys.exit(1)

    category = sys.argv[1]
    subcategory = sys.argv[2]

    if sys.argv[2] == 'all':
        for subcategory in FILTERS[category]:
            update_raw_data(category, subcategory)
    else:
        update_raw_data(category, subcategory)