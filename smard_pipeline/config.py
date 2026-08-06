from pathlib import Path
from typing import TypedDict

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw_data"
PREPROCESSED_DATA_DIR = DATA_DIR / "preprocessed_data"
LOGS_DIR = DATA_DIR / "logs"
COMBINED_HISTORICAL: str = 'combined_historical.parquet'
NUCLEAR_HISTORICAL: str = '1224_historical.parquet'
MARKET_PRICE_HISTORICAL: str = '4169_historical.parquet'

# Current files
COMBINED_CURRENT: str = 'combined_current.parquet'
MARKET_PRICE_CURRENT: str = '4169_current.parquet'

# S3 prefixes
S3_PREFIX_HISTORICAL: str = 'historical/'
S3_PREFIX_CURRENT: str = 'current/'

# Define classes
class TimeSeriesConfig(TypedDict):
    id: int
    include_in_table: bool
    daily_download: bool

# base url of the SMARD API.
BASE_URL: str = "https://www.smard.de/app"

CATEGORIES: dict[str, dict[str, TimeSeriesConfig ]] = {
    'Stromerzeugung': {
        'Braunkohle': TimeSeriesConfig(
            id=1223,
            include_in_table=True,
            daily_download=True
        ),
        'Kernenergie': TimeSeriesConfig(
            id=1224,
            include_in_table=False,
            daily_download=False
        ),
        'Wind Offshore': TimeSeriesConfig(
            id=1225,
            include_in_table=True,
            daily_download=True
        ),
        'Wasserkraft': TimeSeriesConfig(
            id=1226,
            include_in_table=True,
            daily_download=True
        ),
        'Sonstige Konventionelle': TimeSeriesConfig(
            id=1227,
            include_in_table=True,
            daily_download=True
        ),
        'Sonstige Erneuerbare': TimeSeriesConfig(
            id=1228,
            include_in_table=True,
            daily_download=True
        ),
        'Biomasse': TimeSeriesConfig(
            id=4066,
            include_in_table=True,
            daily_download=True
        ),
        'Wind Onshore': TimeSeriesConfig(
            id=4067,
            include_in_table=True,
            daily_download=True
        ),
        'Photovoltaik': TimeSeriesConfig(
            id=4068,
            include_in_table=True,
            daily_download=True
        ),
        'Steinkohle': TimeSeriesConfig(
            id=4069,
            include_in_table=True,
            daily_download=True
        ),
        'Pumpspeicher': TimeSeriesConfig(
            id=4070,
            include_in_table=True,
            daily_download=True
        ),
        'Erdgas': TimeSeriesConfig(
            id=4071,
            include_in_table=True,
            daily_download=True
        ),
    },
    'Stromverbrauch': {
        'Gesamt (Netzlast)': TimeSeriesConfig(
            id=410,
            include_in_table=True,
            daily_download=True
        ),
        'Residuallast': TimeSeriesConfig(
            id=4359,
            include_in_table=True,
            daily_download=True
        ),
        'Pumpspeicher': TimeSeriesConfig(
            id=4387,
            include_in_table=False,
            daily_download=False
        )
    },
    'Marktpreis': {
        'Deutschland-Luxemburg': TimeSeriesConfig(
            id=4169,
            include_in_table=False,
            daily_download=True
        ),
        'Anrainer DE-LU': TimeSeriesConfig(
            id=5078,
            include_in_table=False,
            daily_download=False
        ),
        'Belgien': TimeSeriesConfig(
            id=4996,
            include_in_table=False,
            daily_download=False
        ),
        'Norwegen 2': TimeSeriesConfig(
            id=4997,
            include_in_table=False,
            daily_download=False
        ),
        'Österreich': TimeSeriesConfig(
            id=4170,
            include_in_table=False,
            daily_download=False
        ),
        'Dänemark 1': TimeSeriesConfig(
            id=252,
            include_in_table=False,
            daily_download=False
        ),
        'Dänemark 2': TimeSeriesConfig(
            id=253,
            include_in_table=False,
            daily_download=False
        ),
        'Frankreich': TimeSeriesConfig(
            id=254,
            include_in_table=False,
            daily_download=False
        ),
        'Italien (Nord)': TimeSeriesConfig(
            id=255,
            include_in_table=False,
            daily_download=False
        ),
        'Niederlande': TimeSeriesConfig(
            id=256,
            include_in_table=False,
            daily_download=False
        ),
        'Polen 1': TimeSeriesConfig(
            id=257,
            include_in_table=False,
            daily_download=False
        ),
        'Polen 2': TimeSeriesConfig(
            id=258,
            include_in_table=False,
            daily_download=False
        ),
        'Schweiz': TimeSeriesConfig(
            id=259,
            include_in_table=False,
            daily_download=False
        ),
        'Slowenien': TimeSeriesConfig(
            id=260,
            include_in_table=False,
            daily_download=False
        ),
        'Tschechien': TimeSeriesConfig(
            id=261,
            include_in_table=False,
            daily_download=False
        ),
        'Ungarn': TimeSeriesConfig(
            id=262,
            include_in_table=False,
            daily_download=False
        )
    },
    'Prognostizierte Erzeugung': {
        'Offshore': TimeSeriesConfig(
            id=3791,
            include_in_table=False,
            daily_download=False
        ),
        'Onshore': TimeSeriesConfig(
            id=123,
            include_in_table=False,
            daily_download=False
        ),
        'Photovoltaik': TimeSeriesConfig(
            id=125,
            include_in_table=False,
            daily_download=False
        ),
        'Sonstige': TimeSeriesConfig(
            id=715,
            include_in_table=False,
            daily_download=False
        ),
        'Wind und Photovoltaik': TimeSeriesConfig(
            id=5097,
            include_in_table=False,
            daily_download=False
        ),
        'Gesamt': TimeSeriesConfig(
            id=122,
            include_in_table=False,
            daily_download=False
        )
    }
}

REGIONS: dict[str, str] = {
    'Deutschland': 'DE',
    'Österreich': 'AT',
    'Luxemburg': 'LU',
    'Marktgebiet: DE/LU (ab 01.10.2018)': 'DE-LU',
    'Marktgebiet: DE/AT/LU (bis 30.09.2018)': 'DE-AT-LU',
    'Regelzone (DE): 50Hertz': '50Hertz',
    'Regelzone (DE): Amprion': 'Amprion',
    'Regelzone (DE): TenneT': 'TenneT',
    'Regelzone (DE): TransnetBW': 'TransnetBW',
    'Regelzone (AT): APG': 'APG',
    'Regelzone (LU): Creos': 'Creos'
}

RESOLUTIONS: dict[str, str] = {
    'Stündlich': 'hour',
    'Viertelstündlich': 'quarterhour',
    'Täglich': 'day',
    'Wöchentlich': 'week',
    'Monatlich': 'month',
    'Jährlich': 'year'
}

PATH_DICT: dict[str, str] = {
    'Stromerzeugung': 'power_generation',
    'Stromverbrauch': 'power_consumption',
    'Marktpreis': 'market_price',
    'Prognostizierte Erzeugung': 'forecasted_generation'
}
