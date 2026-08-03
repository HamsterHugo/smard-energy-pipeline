const isLocal = window.location.hostname === 'localhost' ||
                window.location.hostname === '127.0.0.1';

const API_URL = isLocal
    ? 'http://localhost:5000'
    : 'https://PLACEHOLDER.execute-api.us-east-1.amazonaws.com';

const DATA_START_DATE = '2015-01-01';
const NUCLEAR_END_DATE = '2023-04-16';

const GENERATION_SOURCES = [
    { key: 'Photovoltaik', color: '#EF9F27' },
    { key: 'Wind Onshore', color: '#1D9E75' },
    { key: 'Wind Offshore', color: '#185FA5' },
    { key: 'Biomasse', color: '#6DBE45' },
    { key: 'Wasserkraft', color: '#45B8D8' },
    { key: 'Pumpspeicher', color: '#9B59B6' },
    { key: 'Sonstige Erneuerbare', color: '#A8D8A8' },
    { key: 'Erdgas', color: '#E67E22' },
    { key: 'Steinkohle', color: '#7F8C8D' },
    { key: 'Braunkohle', color: '#8B4513' },
    { key: 'Sonstige Konventionelle', color: '#BDC3C7' },
];
const NUCLEAR_SOURCE = { key: 'Kernenergie', color: '#FF6B6B' };

const ENGLISH_MAPPING = {
    'Photovoltaik': 'Photovoltaics (PV)',
    'Wind Onshore': 'Wind Onshore',
    'Wind Offshore': 'Wind Offshore',
    'Biomasse': 'Biomass',
    'Wasserkraft': 'Hydropower',
    'Pumpspeicher': 'Pumped Storage',
    'Sonstige Erneuerbare': 'Other Renewables',
    'Erdgas': 'Natural Gas',
    'Steinkohle': 'Hard Coal',
    'Braunkohle': 'Lignite',
    'Sonstige Konventionelle': 'Other Conventional',
    'Kernenergie': 'Nuclear Energy'
};

const LAYOUT_BASE = {
    paper_bgcolor: '#16213e',
    plot_bgcolor: '#16213e',
    font: { color: '#e0e0e0' },
    margin: { t: 10, r: 20, b: 80, l: 60 },
    legend: { bgcolor: '#16213e' },
    xaxis: {
        title: 'Time',
        tickangle: 0,
        autorange: true,
        rangeslider: { visible: false }
    }
};