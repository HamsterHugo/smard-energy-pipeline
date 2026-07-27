BASE_URL: str = "https://www.smard.de/app"

FILTERS: dict[str, dict[str, int]] = {
    'Stromerzeugung': {
        'Braunkohle': 1223,
        'Kernenergie': 1224,
        'Wind Offshore': 1225,
        'Wasserkraft': 1226,
        'Sonstige Konventionelle': 1227,
        'Sonstige Erneuerbare': 1228,
        'Biomasse': 4066,
        'Wind Onshore': 4067,
        'Photovoltaik': 4068,
        'Steinkohle': 4069,
        'Pumpspeicher': 4070,
        'Erdgas': 4071,
    },
    'Stromverbrauch': {
        'Gesamt (Netzlast)': 410,
        'Residuallast': 4359,
        'Pumpspeicher': 4387
    },
    'Marktpreis': {
        'Deutschland/Luxemburg': 4169,
        'Anrainer DE/LU': 5078,
        'Belgien': 4996,
        'Norwegen 2': 4997,
        'Österreich': 4170,
        'Dänemark 1': 252,
        'Dänemark 2': 253,
        'Frankreich': 254,
        'Italien (Nord)': 255,
        'Niederlande': 256,
        'Polen 1': 257,
        'Polen 2': 258,
        'Schweiz': 259,
        'Slowenien': 260,
        'Tschechien': 261,
        'Ungarn': 262
    },
    'Prognostizierte Erzeugung': {
        'Offshore': 3791,
        'Onshore': 123,
        'Photovoltaik': 125,
        'Sonstige': 715,
        'Wind und Photovoltaik': 5097,
        'Gesamt': 122
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