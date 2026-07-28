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
    convert_timestamps: bool

class EnergyTimeSeriesConfig(TimeSeriesConfig):
    active: bool
    deprecated_since: str | None

# base url of the SMARD API.
BASE_URL: str = "https://www.smard.de/app"

CATEGORIES: dict[str, dict[str, TimeSeriesConfig | EnergyTimeSeriesConfig]] = {
    'Stromerzeugung': {
        'Braunkohle': EnergyTimeSeriesConfig(
            id=1223,
            convert_timestamps=False,
            active=True,
            deprecated_since=None
        ),
        'Kernenergie': EnergyTimeSeriesConfig(
            id=1224,
            convert_timestamps=True,
            active=False,
            deprecated_since="2023-04-16 0:00"
        ),
        'Wind Offshore': EnergyTimeSeriesConfig(
            id=1225,
            convert_timestamps=False,
            active=True,
            deprecated_since=None
        ),
        'Wasserkraft': EnergyTimeSeriesConfig(
            id=1226,
            convert_timestamps=False,
            active=True,
            deprecated_since=None
        ),
        'Sonstige Konventionelle': EnergyTimeSeriesConfig(
            id=1227,
            convert_timestamps=False,
            active=True,
            deprecated_since=None
        ),
        'Sonstige Erneuerbare': EnergyTimeSeriesConfig(
            id=1228,
            convert_timestamps=False,
            active=True,
            deprecated_since=None
        ),
        'Biomasse': EnergyTimeSeriesConfig(
            id=4066,
            convert_timestamps=False,
            active=True,
            deprecated_since=None
        ),
        'Wind Onshore': EnergyTimeSeriesConfig(
            id=4067,
            convert_timestamps=False,
            active=True,
            deprecated_since=None
        ),
        'Photovoltaik': EnergyTimeSeriesConfig(
            id=4068,
            convert_timestamps=False,
            active=True,
            deprecated_since=None
        ),
        'Steinkohle': EnergyTimeSeriesConfig(
            id=4069,
            convert_timestamps=False,
            active=True,
            deprecated_since=None
        ),
        'Pumpspeicher': EnergyTimeSeriesConfig(
            id=4070,
            convert_timestamps=False,
            active=True,
            deprecated_since=None
        ),
        'Erdgas': EnergyTimeSeriesConfig(
            id=4071,
            convert_timestamps=False,
            active=True,
            deprecated_since=None
        ),
    },
    'Stromverbrauch': {
        'Gesamt (Netzlast)': TimeSeriesConfig(
            id=410,
            convert_timestamps=False
        ),
        'Residuallast': TimeSeriesConfig(
            id=4359,
            convert_timestamps=False
        ),
        'Pumpspeicher': TimeSeriesConfig(
            id=4387,
            convert_timestamps=False
        )
    },
    'Marktpreis': {
        'Deutschland-Luxemburg': TimeSeriesConfig(
            id=4169,
            convert_timestamps=True
        ),
        'Anrainer DE-LU': TimeSeriesConfig(
            id=5078,
            convert_timestamps=True
        ),
        'Belgien': TimeSeriesConfig(
            id=4996,
            convert_timestamps=True
        ),
        'Norwegen 2': TimeSeriesConfig(
            id=4997,
            convert_timestamps=True
        ),
        'Österreich': TimeSeriesConfig(
            id=4170,
            convert_timestamps=True
        ),
        'Dänemark 1': TimeSeriesConfig(
            id=252,
            convert_timestamps=True
        ),
        'Dänemark 2': TimeSeriesConfig(
            id=253,
            convert_timestamps=True
        ),
        'Frankreich': TimeSeriesConfig(
            id=254,
            convert_timestamps=True
        ),
        'Italien (Nord)': TimeSeriesConfig(
            id=255,
            convert_timestamps=True
        ),
        'Niederlande': TimeSeriesConfig(
            id=256,
            convert_timestamps=True
        ),
        'Polen 1': TimeSeriesConfig(
            id=257,
            convert_timestamps=True
        ),
        'Polen 2': TimeSeriesConfig(
            id=258,
            convert_timestamps=True
        ),
        'Schweiz': TimeSeriesConfig(
            id=259,
            convert_timestamps=True
        ),
        'Slowenien': TimeSeriesConfig(
            id=260,
            convert_timestamps=True
        ),
        'Tschechien': TimeSeriesConfig(
            id=261,
            convert_timestamps=True
        ),
        'Ungarn': TimeSeriesConfig(
            id=262,
            convert_timestamps=True
        )
    },
    'Prognostizierte Erzeugung': {
        'Offshore': TimeSeriesConfig(
            id=3791,
            convert_timestamps=False
        ),
        'Onshore': TimeSeriesConfig(
            id=123,
            convert_timestamps=False
        ),
        'Photovoltaik': TimeSeriesConfig(
            id=125,
            convert_timestamps=False
        ),
        'Sonstige': TimeSeriesConfig(
            id=715,
            convert_timestamps=False
        ),
        'Wind und Photovoltaik': TimeSeriesConfig(
            id=5097,
            convert_timestamps=False
        ),
        'Gesamt': TimeSeriesConfig(
            id=122,
            convert_timestamps=False
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
