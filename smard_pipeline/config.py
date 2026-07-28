from pathlib import Path
from typing import TypedDict

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw_data"
PREPROCESSED_DATA_DIR = DATA_DIR / "preprocessed_data"
LOGS_DIR = DATA_DIR / "logs"

# Define classes
class TimeSeriesConfig(TypedDict):
    id: int
    include_in_table: bool

class EnergyTimeSeriesConfig(TimeSeriesConfig):
    active: bool
    deprecated_since: str | None

# base url of the SMARD API.
BASE_URL: str = "https://www.smard.de/app"

CATEGORIES: dict[str, dict[str, TimeSeriesConfig | EnergyTimeSeriesConfig]] = {
    'Stromerzeugung': {
        'Braunkohle': EnergyTimeSeriesConfig(
            id=1223,
            include_in_table=True,
            active=True,
            deprecated_since=None
        ),
        'Kernenergie': EnergyTimeSeriesConfig(
            id=1224,
            include_in_table=False,
            active=False,
            deprecated_since="2023-04-16 0:00"
        ),
        'Wind Offshore': EnergyTimeSeriesConfig(
            id=1225,
            include_in_table=True,
            active=True,
            deprecated_since=None
        ),
        'Wasserkraft': EnergyTimeSeriesConfig(
            id=1226,
            include_in_table=True,
            active=True,
            deprecated_since=None
        ),
        'Sonstige Konventionelle': EnergyTimeSeriesConfig(
            id=1227,
            include_in_table=True,
            active=True,
            deprecated_since=None
        ),
        'Sonstige Erneuerbare': EnergyTimeSeriesConfig(
            id=1228,
            include_in_table=True,
            active=True,
            deprecated_since=None
        ),
        'Biomasse': EnergyTimeSeriesConfig(
            id=4066,
            include_in_table=True,
            active=True,
            deprecated_since=None
        ),
        'Wind Onshore': EnergyTimeSeriesConfig(
            id=4067,
            include_in_table=True,
            active=True,
            deprecated_since=None
        ),
        'Photovoltaik': EnergyTimeSeriesConfig(
            id=4068,
            include_in_table=True,
            active=True,
            deprecated_since=None
        ),
        'Steinkohle': EnergyTimeSeriesConfig(
            id=4069,
            include_in_table=True,
            active=True,
            deprecated_since=None
        ),
        'Pumpspeicher': EnergyTimeSeriesConfig(
            id=4070,
            include_in_table=True,
            active=True,
            deprecated_since=None
        ),
        'Erdgas': EnergyTimeSeriesConfig(
            id=4071,
            include_in_table=True,
            active=True,
            deprecated_since=None
        ),
    },
    'Stromverbrauch': {
        'Gesamt (Netzlast)': TimeSeriesConfig(
            id=410,
            include_in_table=True
        ),
        'Residuallast': TimeSeriesConfig(
            id=4359,
            include_in_table=True
        ),
        'Pumpspeicher': TimeSeriesConfig(
            id=4387,
            include_in_table=False
        )
    },
    'Marktpreis': {
        'Deutschland-Luxemburg': TimeSeriesConfig(
            id=4169,
            include_in_table=False
        ),
        'Anrainer DE-LU': TimeSeriesConfig(
            id=5078,
            include_in_table=False
        ),
        'Belgien': TimeSeriesConfig(
            id=4996,
            include_in_table=False
        ),
        'Norwegen 2': TimeSeriesConfig(
            id=4997,
            include_in_table=False
        ),
        'Österreich': TimeSeriesConfig(
            id=4170,
            include_in_table=False
        ),
        'Dänemark 1': TimeSeriesConfig(
            id=252,
            include_in_table=False
        ),
        'Dänemark 2': TimeSeriesConfig(
            id=253,
            include_in_table=False
        ),
        'Frankreich': TimeSeriesConfig(
            id=254,
            include_in_table=False
        ),
        'Italien (Nord)': TimeSeriesConfig(
            id=255,
            include_in_table=False
        ),
        'Niederlande': TimeSeriesConfig(
            id=256,
            include_in_table=False
        ),
        'Polen 1': TimeSeriesConfig(
            id=257,
            include_in_table=False
        ),
        'Polen 2': TimeSeriesConfig(
            id=258,
            include_in_table=False
        ),
        'Schweiz': TimeSeriesConfig(
            id=259,
            include_in_table=False
        ),
        'Slowenien': TimeSeriesConfig(
            id=260,
            include_in_table=False
        ),
        'Tschechien': TimeSeriesConfig(
            id=261,
            include_in_table=False
        ),
        'Ungarn': TimeSeriesConfig(
            id=262,
            include_in_table=False
        )
    },
    'Prognostizierte Erzeugung': {
        'Offshore': TimeSeriesConfig(
            id=3791,
            include_in_table=False
        ),
        'Onshore': TimeSeriesConfig(
            id=123,
            include_in_table=False
        ),
        'Photovoltaik': TimeSeriesConfig(
            id=125,
            include_in_table=False
        ),
        'Sonstige': TimeSeriesConfig(
            id=715,
            include_in_table=False
        ),
        'Wind und Photovoltaik': TimeSeriesConfig(
            id=5097,
            include_in_table=False
        ),
        'Gesamt': TimeSeriesConfig(
            id=122,
            include_in_table=False
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
