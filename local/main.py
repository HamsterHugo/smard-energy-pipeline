import sys
import logging

from downloader import update_raw_data, download_current_week
from smard_pipeline.config import CATEGORIES
from smard_pipeline.transformations import merge_raw_data, combine_data
from smard_pipeline.logging_config import setup_logging, save_log_to_html

usage: str = """
USAGE:
    python main.py historical <category> <subcategory>
    python main.py historical <category> all
    python main.py historical combine
    pyhton main.py merge <category> <subcategory>
    python main.py merge <category> all
    python main.py current <category> <subcategory>
    python main.py current <category> all
    python main.py current combine
"""

functions = {
    'historical': update_raw_data,
    'merge': merge_raw_data,
    'current': download_current_week
}

setup_logging(level=logging.INFO)

if __name__ == '__main__':
    if (len(sys.argv) not in [3,4]
        or sys.argv[1] not in functions
        or (sys.argv[2] == 'combine'
            and sys.argv[1] not in ['historical', 'current'])):
        print(usage)
        sys.exit(1)

    logger = logging.getLogger(__name__)

    if len(sys.argv) == 4:
        category: str = sys.argv[2]
        subcategory: str = sys.argv[3]
        f: function = functions[sys.argv[1]]

        if subcategory == 'all':
            for current_subcategory in CATEGORIES[category]:
                f(category, current_subcategory)
        else:
            f(category, subcategory)
    else:
        combine_data(sys.argv[1])

    save_log_to_html('_'.join(sys.argv[1:]))

