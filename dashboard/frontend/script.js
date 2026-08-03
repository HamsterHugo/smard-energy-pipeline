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

// On loading: Set the last 7 days.
window.onload = function () {
    setLastDays(7);
};

function setLastDays(days) {
    const to = new Date();
    const from = new Date();
    from.setDate(from.getDate() - days);

    document.getElementById('date-to').value = to.toISOString().split('T')[0];
    document.getElementById('date-from').value = from.toISOString().split('T')[0];

    loadData();
}

function showLoading() {
    document.getElementById('loading-overlay').classList.add('visible');
    document.body.style.cursor = 'wait';
}

function hideLoading() {
    document.getElementById('loading-overlay').classList.remove('visible');
    document.body.style.cursor = 'default';
}

async function loadData() {
    showLoading();
    try {
        const from = document.getElementById('date-from').value;
        const to = document.getElementById('date-to').value;

        // Kernenergie nur abfragen wenn Zeitraum vor Abschaltdatum liegt
        const needsNuclear = from < NUCLEAR_END_DATE;

        const requests = [
            fetch(`${API_URL}/data?from=${from}&to=${to}`),
            fetch(`${API_URL}/price?from=${from}&to=${to}`)
        ];

        if (needsNuclear) {
            requests.push(fetch(`${API_URL}/nuclear?from=${from}&to=${to}`));
        }

        const responses = await Promise.all(requests);
        const data = await responses[0].json();
        const priceData = await responses[1].json();
        const nuclearData = needsNuclear ? await responses[2].json() : [];

        updateMetrics(data, priceData);
        renderCharts(data, priceData, nuclearData);
    }
    finally {
        hideLoading();
    }
}

function updateMetrics(data, priceData) {
    const from = document.getElementById('date-from').value;

    // No data before 2015
    if (from < DATA_START_DATE) {
        document.getElementById('metric-generation').textContent = '—';
        document.getElementById('metric-renewables').textContent = '—';
        document.getElementById('metric-price').textContent = '—';
        document.getElementById('metric-consumption').textContent = '—';
        return;
    }

    // Renewable scoureces
    const RENEWABLE_SOURCES = [
        'Photovoltaik', 'Wind Onshore', 'Wind Offshore',
        'Biomasse', 'Wasserkraft', 'Pumpspeicher', 'Sonstige Erneuerbare'
    ];

    // Total generation at time
    const generationPerRow = data.map(d =>
        GENERATION_SOURCES.reduce((sum, s) => sum + (d[s.key] ?? 0), 0)
    );

    // Renewable energies at time
    const renewablesPerRow = data.map(d =>
        RENEWABLE_SOURCES.reduce((sum, key) => sum + (d[key] ?? 0), 0)
    );

    // Compute sums
    const totalGeneration = generationPerRow.reduce((a, b) => a + b, 0);
    const totalRenewables = renewablesPerRow.reduce((a, b) => a + b, 0);
    const totalConsumption = data.reduce((sum, d) => sum + (d['Gesamt (Netzlast)'] ?? 0), 0);

    // Renewable energies percentage
    const renewablesShare = totalGeneration > 0
        ? (totalRenewables / totalGeneration * 100).toFixed(1)
        : 0;

    // Average marketprice
    const avgPrice = priceData.length > 0
        ? (priceData.reduce((sum, d) => sum + (d['Deutschland-Luxemburg'] ?? 0), 0) / priceData.length).toFixed(2)
        : null;

    // Metrics
    document.getElementById('metric-generation').textContent =
        (totalGeneration / 1_000_000).toFixed(2) + ' TWh';
    document.getElementById('metric-renewables').textContent =
        renewablesShare + ' %';
    document.getElementById('metric-price').textContent =
        avgPrice !== null ? avgPrice + ' €/MWh' : '—';
    document.getElementById('metric-consumption').textContent =
        (totalConsumption / 1_000_000).toFixed(2) + ' TWh';
}