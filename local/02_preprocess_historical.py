import sys

from smard_pipeline.config import FILTERS
from smard_pipeline.transformations import merge_raw_data

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python 02_preprocess_historical.py <category> <subcategory>")
        print("Example: python 02_preprocess_historical.py Stromerzeugung Erdgas")
        print("Example: python 02_preprocess_historical.py Stromverbrauch Residuallast")
        print('For looping through all subcategories use:')
        print('python 02_preprocess_historical.py <category> all')
        sys.exit(1)

    category = sys.argv[1]
    subcategory = sys.argv[2]

    if sys.argv[2] == 'all':
        for subcategory in FILTERS[category]:
            merge_raw_data(category, subcategory)
    else:
        merge_raw_data(category, subcategory)