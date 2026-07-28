import sys

from smard_pipeline.config import FILTERS
from smard_pipeline.transformations import merge_raw_data, merge_all_categories

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'combine':
        merge_all_categories()

    elif len(sys.argv) == 3:
        category = sys.argv[1]
        subcategory = sys.argv[2]

        if subcategory == 'all':
            for current_subcategory in FILTERS[category]:
                merge_raw_data(category, current_subcategory)
        else:
            merge_raw_data(category, subcategory)

    else:
        print("Usage:")
        print("  python 02_preprocess_historical.py <category> <subcategory>")
        print("  python 02_preprocess_historical.py <category> all")
        print("  python 02_preprocess_historical.py combine")
        sys.exit(1)